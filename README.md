# **Web Crawler API**

Welcome to the **Web Crawler API**! This project allows you to crawl any webpage, extract links from it, and return them in a structured JSON format. You can customize various parameters like the depth of the crawl, number of pages, and whether to respect the website's `robots.txt` rules.
API Service Link: https://web-crawler-b5zg.onrender.com/api/crawl
---

## **How This Project Works**

This API is built using Python and Flask, with asynchronous crawling using `aiohttp` to make it efficient and scalable. The crawler starts at the specified root URL, explores all links up to a given depth, and returns the results in JSON format.

Here’s a breakdown of how it works:
1. **Root URL**: The starting point for the crawler.
2. **Depth**: Specifies how many levels of links should be followed (e.g., if `max_depth = 2`, it will crawl links on the root page and the links found on those pages).
3. **Link Extraction**: As the crawler visits each page, it extracts all the hyperlinks (`<a href="...">`) from the HTML content.
4. **Response**: The API returns a JSON object that includes the crawled links, their HTTP headers, and any errors encountered during the crawl.

---

## **Files and Structure**

Here’s how each file contributes to the project:

### **1. `app.py`**

This is the main entry point for the Flask application. It defines the API endpoint `/api/crawl` and handles the requests from users. It extracts parameters from the request body and triggers the crawler.

### **2. `crawler/`**

This folder contains the core functionality of the crawler.

- **`crawler.py`**: This file defines the `WebCrawler` class, which contains the logic for asynchronously crawling web pages. It fetches URLs, extracts links, and stores metadata like HTTP headers.
  
- **`utils.py`**: Contains helper functions such as URL normalization and domain checking.

- **`robots.py`**: Handles the logic for checking the `robots.txt` file to see if the crawler is allowed to access certain pages.

### **3. `requirements.txt`**

This file lists all the Python dependencies required to run the project. Flask is used for the API, and `aiohttp` for making asynchronous HTTP requests.

### **4. `Procfile`**

The `Procfile` is used for deployment on platforms like Render. It tells the platform how to run the application using `gunicorn` to serve the Flask app in production.

---

## **API Usage**

### **POST /api/crawl**

This is the main endpoint you will use to crawl web pages. You can customize the crawl by specifying several parameters.

#### **Request Parameters**

- **root_url** (String, Required): The starting point for the crawler.
- **max_depth** (Integer, Required): The depth to which the crawler should traverse from the root URL.
- **max_pages** (Integer, Optional): Maximum number of pages to crawl (default is 100).
- **allowed_domains** (Array of Strings, Optional): Restrict the crawler to specific domains.
- **exclude_patterns** (Array of Strings, Optional): Regex patterns to exclude certain URLs (e.g., exclude images, CSS).
- **include_patterns** (Array of Strings, Optional): Regex patterns to specifically include certain URLs.
- **user_agent** (String, Optional): Custom User-Agent header for HTTP requests (default is `WebCrawlerBot/1.0`).
- **respect_robots** (Boolean, Optional): Whether to respect `robots.txt` rules (default is true).
- **timeout** (Integer, Optional): Request timeout for HTTP calls (default is 10 seconds).
- **concurrency** (Integer, Optional): Number of concurrent requests (default is 5).

#### **Example Request (cURL)**

```bash
curl -X POST https://your-app.onrender.com/api/crawl](https://web-crawler-b5zg.onrender.com/api/crawl \
-H "Content-Type: application/json" \
-d '{
  "root_url": "https://example.com",
  "max_depth": 2
}'
```

### **Example JSON Response**

Here's an example of a response when crawling `https://www.youtube.com`:

```json
{
    "data": {
        "crawled_links": [{
            "depth": 0,
            "headers": {
                "Cache-Control": "no-cache, no-store, max-age=0, must-revalidate",
                "Content-Type": "text/html; charset=utf-8",
                "Date": "Mon, 21 Oct 2024 21:55:05 GMT",
                "Set-Cookie": "GPS=1; Domain=.youtube.com; Expires=Mon, 21-Oct-2024 22:25:05 GMT; Path=/; Secure; HttpOnly"
            },
            "links_found": [
                "https://www.youtube.com/t/contact_us",
                "https://www.youtube.com/t/privacy",
                "https://www.youtube.com/about",
                "https://www.youtube.com/ads"
            ],
            "status_code": 200,
            "url": "https://www.youtube.com"
        }],
        "errors": []
    },
    "status": "success"
}
```

#### **Explanation of the Response**

- **`crawled_links`**: This is the list of links that the crawler found at the root URL.
  - **`depth`**: The depth level at which this page was found.
  - **`headers`**: The HTTP headers returned by the server when visiting the page.
  - **`links_found`**: The list of links extracted from this page.
  - **`status_code`**: The HTTP status code (e.g., 200 means the request was successful).
  - **`url`**: The URL that was crawled.
  
- **`errors`**: If any errors occur during the crawl (e.g., broken links, timeouts), they will be listed here.
  
---

## **Where to See Crawled Links**

In the JSON response, you can view all the crawled links in the `"crawled_links"` array. Each entry contains:
- **`url`**: The URL that was crawled.
- **`links_found`**: A list of all the URLs found on the page.

For example, in the above response, the page `https://www.youtube.com` returned a list of links such as:
- `https://www.youtube.com/t/contact_us`
- `https://www.youtube.com/t/privacy`
- `https://www.youtube.com/about`

You can easily parse this JSON response to extract and use the crawled links as needed.

---

## **Running the Project Locally**

### **1. Clone the Repository**

```bash
git clone {this repo link}
cd web_crawler_api
```

### **2. Create and Activate a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Run the Flask Application**

```bash
python app.py
```

The app will now be running on `http://localhost:5000`.

### **5. Test Locally Using cURL**

You can send POST requests to test the API running on your local machine.

```bash
curl -X POST http://localhost:5000/api/crawl \
-H "Content-Type: application/json" \
-d '{
  "root_url": "https://example.com",
  "max_depth": 2
}'
```

---

## **Deploying the Project on Render**

### **Step 1: Push Code to GitHub**

Ensure your code is pushed to a GitHub repository:

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

## **Conclusion**

This project provides a flexible and scalable way to crawl websites and extract links. It can be deployed locally or on cloud platforms like Render. You can customize the crawl by setting parameters like the depth, maximum pages, user-agent, and more.

Feel free to reach out if you have any questions, or if you'd like assistance with setting up or extending this project!

---

## **Contact**

For any questions or support:

- **Email**: bhuwanawasthi2021@gmail.com

