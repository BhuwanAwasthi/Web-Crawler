# crawler/crawler.py

import asyncio
import aiohttp
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import re
from crawler.utils import normalize_url, is_allowed_domain
from crawler.robots import RobotsParser
import logging

class WebCrawler:
    def __init__(self, root_url, max_depth, max_pages, allowed_domains, exclude_patterns,
                 include_patterns, user_agent, respect_robots, timeout, concurrency):
        self.root_url = normalize_url(root_url)
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.allowed_domains = allowed_domains
        self.exclude_patterns = [re.compile(p) for p in exclude_patterns]
        self.include_patterns = [re.compile(p) for p in include_patterns]
        self.user_agent = user_agent
        self.respect_robots = respect_robots
        self.timeout = timeout
        self.concurrency = concurrency

        self.visited = set()
        self.crawled_links = []
        self.errors = []
        self.semaphore = asyncio.Semaphore(concurrency)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        if self.respect_robots:
            self.robots_parser = RobotsParser(self.user_agent)
            self.robots_parser.fetch_robots_txt(self.root_url)

    def start(self):
        try:
            self.loop.run_until_complete(self.crawl())
            return {
                'crawled_links': self.crawled_links,
                'errors': self.errors
            }
        finally:
            self.loop.close()

    async def crawl(self):
        queue = asyncio.Queue()
        await queue.put((self.root_url, 0))

        tasks = []
        while not queue.empty() and len(self.visited) < self.max_pages:
            current_url, depth = await queue.get()
            if depth > self.max_depth or current_url in self.visited:
                continue
            self.visited.add(current_url)
            task = asyncio.create_task(self.fetch_and_parse(current_url, depth, queue))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def fetch_and_parse(self, url, depth, queue):
        async with self.semaphore:
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout),
                                                 headers={'User-Agent': self.user_agent}) as session:
                    if self.respect_robots and not self.robots_parser.is_allowed(url):
                        logging.info(f"Blocked by robots.txt: {url}")
                        return
                    async with session.get(url) as response:
                        status_code = response.status
                        headers = dict(response.headers)
                        content_type = headers.get('Content-Type', '')
                        links_found = []
                        if 'text/html' in content_type:
                            html = await response.text()
                            links = self.extract_links(html, url)
                            for link in links:
                                if link not in self.visited:
                                    await queue.put((link, depth + 1))
                                    links_found.append(link)
                        self.crawled_links.append({
                            'url': url,
                            'depth': depth,
                            'status_code': status_code,
                            'links_found': links_found,
                            'headers': headers
                        })
            except Exception as e:
                self.errors.append({
                    'url': url,
                    'error': str(e)
                })
                logging.exception(f"Error fetching {url}")

    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            link = normalize_url(urljoin(base_url, href))
            if self.is_valid_link(link):
                links.add(link)
        return links

    def is_valid_link(self, link):
        # Check domain
        if not is_allowed_domain(link, self.allowed_domains):
            return False
        # Exclude patterns
        if any(pattern.match(link) for pattern in self.exclude_patterns):
            return False
        # Include patterns
        if self.include_patterns and not any(pattern.match(link) for pattern in self.include_patterns):
            return False
        return True
