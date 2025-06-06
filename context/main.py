import json
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tempfile import mkdtemp
import time


def handler(event=None, context=None):
    """
    Lambda handler for web scraping with Selenium
    Supports both direct Lambda invocation and API Gateway events

    Event payload structure (for direct invocation):
    {
        "url": "https://example.com",                 # Required: Target URL
        "method": "GET",                              # Optional: HTTP method (GET, POST)
        "output_type": "text",                        # Optional: text, screenshot, both
        "selector": "html",                           # Optional: CSS selector or XPath
        "wait_for": null,                             # Optional: CSS selector to wait for
        "wait_timeout": 10,                           # Optional: Wait timeout in seconds
        "viewport": {"width": 1280, "height": 1696},  # Optional: Browser viewport
        "headers": {},                                # Optional: Custom headers
        "cookies": [],                                # Optional: Cookies to set
        "form_data": {}                               # Optional: Form data for POST requests
    }

    For API Gateway, the payload should be in event["body"] as JSON string
    """

    try:
        # Handle API Gateway event format
        is_api_gateway = event and "body" in event and "httpMethod" in event

        if is_api_gateway:
            # API Gateway event
            if event["body"]:
                if isinstance(event["body"], str):
                    payload = json.loads(event["body"])
                else:
                    payload = event["body"]
            else:
                payload = {}
        else:
            # Direct Lambda invocation
            payload = event or {}

        # Extract parameters with defaults
        url = payload.get("url")
        method = payload.get("method", "GET").upper()
        output_type = payload.get("output_type", "text")  # text, screenshot, both
        selector = payload.get("selector", "html")
        wait_for = payload.get("wait_for")
        wait_timeout = payload.get("wait_timeout", 10)
        viewport = payload.get("viewport", {"width": 1280, "height": 720})
        headers = payload.get("headers", {})
        cookies = payload.get("cookies", [])
        form_data = payload.get("form_data", {})

        # Setup Chrome options
        options = webdriver.ChromeOptions()
        options.binary_location = "/opt/chrome/chrome"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={viewport['width']}x{viewport['height']}")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")

        # Add custom headers if provided
        if headers:
            for key, value in headers.items():
                options.add_argument(f"--header={key}: {value}")

        # Create service and driver
        service = Service("/opt/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        try:
            # Set viewport size
            driver.set_window_size(viewport["width"], viewport["height"])

            # Add cookies if provided
            if cookies:
                # Navigate to domain first to set cookies
                driver.get(url)
                for cookie in cookies:
                    driver.add_cookie(cookie)

            # Navigate to URL
            if method == "GET":
                driver.get(url)
            else:
                driver.get(url)

            # Wait for specific element if specified
            if wait_for:
                wait = WebDriverWait(driver, wait_timeout)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_for)))

            # Wait for fonts to load
            driver.execute_script(
                """
                if (document.fonts && document.fonts.ready) {
                    return document.fonts.ready;
                }
                return Promise.resolve();
            """
            )

            # Additional small delay to ensure proper rendering
            time.sleep(1)

            # Prepare response
            response = {
                "success": True,
                "url": driver.current_url,
                "title": driver.title,
                "timestamp": int(time.time()),
            }

            # Get text content
            if output_type in ["text", "both"]:
                try:
                    if selector.startswith("//"):
                        # XPath selector
                        element = driver.find_element(By.XPATH, selector)
                    else:
                        # CSS selector
                        element = driver.find_element(By.CSS_SELECTOR, selector)

                    response["text"] = element.text
                    response["html"] = element.get_attribute("innerHTML")
                except Exception as e:
                    response["text"] = driver.find_element(By.TAG_NAME, "body").text
                    response["html"] = driver.page_source
                    response["selector_error"] = str(e)

            # Get screenshot
            if output_type in ["screenshot", "both"]:
                try:
                    screenshot_bytes = driver.get_screenshot_as_png()
                    screenshot_b64 = base64.b64encode(screenshot_bytes).decode("utf-8")
                    response["screenshot"] = screenshot_b64
                    response["screenshot_format"] = "png"
                except Exception as e:
                    response["screenshot_error"] = str(e)

            # Return appropriate format based on event type
            if is_api_gateway:
                return format_api_response(response)
            else:
                return response

        finally:
            driver.quit()

    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "timestamp": int(time.time()),
        }

        # Return appropriate format based on event type
        if "is_api_gateway" in locals() and is_api_gateway:
            return format_api_response(error_response, 500)
        else:
            return error_response


# Helper function to format response for API Gateway
def format_api_response(data, status_code=200):
    """Format response for API Gateway"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(data, ensure_ascii=False),
    }
