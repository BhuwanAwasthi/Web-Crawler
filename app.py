# app.py

from flask import Flask, request, jsonify
from crawler.crawler import WebCrawler
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/api/crawl', methods=['POST'])
def crawl():
    try:
        data = request.get_json()
        # Required parameters
        root_url = data['root_url']
        max_depth = data['max_depth']

        # Optional parameters with defaults
        max_pages = data.get('max_pages', 100)
        allowed_domains = data.get('allowed_domains', [root_url.split('//')[-1].split('/')[0]])
        exclude_patterns = data.get('exclude_patterns', [])
        include_patterns = data.get('include_patterns', [])
        user_agent = data.get('user_agent', 'WebCrawlerBot/1.0')
        respect_robots = data.get('respect_robots', True)
        timeout = data.get('timeout', 10)
        concurrency = data.get('concurrency', 5)

        # Initialize and start the crawler
        crawler = WebCrawler(
            root_url=root_url,
            max_depth=max_depth,
            max_pages=max_pages,
            allowed_domains=allowed_domains,
            exclude_patterns=exclude_patterns,
            include_patterns=include_patterns,
            user_agent=user_agent,
            respect_robots=respect_robots,
            timeout=timeout,
            concurrency=concurrency
        )

        crawled_data = crawler.start()

        return jsonify({
            'status': 'success',
            'data': crawled_data
        }), 200

    except KeyError as e:
        return jsonify({
            'status': 'error',
            'message': f'Missing required parameter: {str(e)}'
        }), 400

    except Exception as e:
        logging.exception("An error occurred during crawling.")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
