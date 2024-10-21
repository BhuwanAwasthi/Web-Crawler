# crawler/robots.py

from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import logging

class RobotsParser:
    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.parsers = {}

    def fetch_robots_txt(self, base_url):
        parsed_url = urlparse(base_url)
        robots_url = urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", '/robots.txt')
        rp = RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
        except Exception as e:
            logging.exception(f"Failed to read robots.txt from {robots_url}")
        self.parsers[parsed_url.netloc] = rp

    def is_allowed(self, url):
        netloc = urlparse(url).netloc
        rp = self.parsers.get(netloc)
        if rp:
            return rp.can_fetch(self.user_agent, url)
        return True  # Allow if robots.txt not found or can't be read
