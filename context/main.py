import json
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tempfile import mkdtemp
import time

# Import custom modules
from font_handler import ChineseFontHandler, ChromeOptionsBuilder
from loading_handler import PageLoadingStrategy, ScreenshotHandler


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
        "page_load_timeout": 30,                      # Optional: Page load timeout in seconds
        "viewport": {"width": 1280, "height": 1696},  # Optional: Browser viewport
        "headers": {},                                # Optional: Custom headers
        "cookies": [],                                # Optional: Cookies to set
        "form_data": {}                               # Optional: Form data for POST requests
    }

    For API Gateway, the payload should be in event["body"] as JSON string
    """

    try:
        # 解析事件格式
        is_api_gateway, payload = _parse_event(event)

        # 提取參數
        params = _extract_parameters(payload)

        # 設定Chrome選項
        options = _setup_chrome_options(params["viewport"], params["headers"])

        # 創建服務和驅動程式
        service = Service("/opt/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        try:
            # 配置驅動程式
            _configure_driver(driver, params)

            # 導航到URL
            _navigate_to_url(driver, params["url"], params["method"])

            # 創建處理器實例
            font_handler = ChineseFontHandler()
            loading_strategy = PageLoadingStrategy(driver)
            screenshot_handler = ScreenshotHandler(driver, font_handler)

            # 執行智能載入策略
            loading_result = loading_strategy.execute_smart_loading(
                wait_for=params["wait_for"], wait_timeout=params["wait_timeout"]
            )

            # 應用字體優化
            font_handler.apply_enhanced_fonts(driver)

            # 準備回應
            response = {
                "success": True,
                "url": driver.current_url,
                "title": driver.title,
                "timestamp": int(time.time()),
                "loading_info": loading_result,
            }

            # 處理文字內容
            if params["output_type"] in ["text", "both"]:
                text_result = _extract_text_content(driver, params["selector"])
                response.update(text_result)

            # 處理截圖
            if params["output_type"] in ["screenshot", "both"]:
                screenshot_result = screenshot_handler.take_screenshot()
                if screenshot_result["success"]:
                    screenshot_b64 = base64.b64encode(screenshot_result["data"]).decode(
                        "utf-8"
                    )
                    response["screenshot"] = screenshot_b64
                    response["screenshot_format"] = "png"
                    response["screenshot_size"] = screenshot_result["size"]
                    if "fallback" in screenshot_result:
                        response["fallback_screenshot"] = True
                else:
                    response["screenshot_error"] = screenshot_result["error"]

            # 返回適當格式
            return _format_response(response, is_api_gateway)

        finally:
            driver.quit()

    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "timestamp": int(time.time()),
        }

        is_api_gateway = "is_api_gateway" in locals() and locals()["is_api_gateway"]
        return _format_response(error_response, is_api_gateway, 500)


def _parse_event(event):
    """解析事件格式"""
    is_api_gateway = event and "body" in event and "httpMethod" in event

    if is_api_gateway:
        if event["body"]:
            if isinstance(event["body"], str):
                payload = json.loads(event["body"])
            else:
                payload = event["body"]
        else:
            payload = {}
    else:
        payload = event or {}

    return is_api_gateway, payload


def _extract_parameters(payload):
    """提取參數並設定預設值"""
    return {
        "url": payload.get("url"),
        "method": payload.get("method", "GET").upper(),
        "output_type": payload.get("output_type", "text"),
        "selector": payload.get("selector", "html"),
        "wait_for": payload.get("wait_for"),
        "wait_timeout": payload.get("wait_timeout", 3),
        "page_load_timeout": payload.get("page_load_timeout", 15),
        "viewport": payload.get("viewport", {"width": 1600, "height": 900}),
        "headers": payload.get("headers", {}),
        "cookies": payload.get("cookies", []),
        "form_data": payload.get("form_data", {}),
    }


def _setup_chrome_options(viewport, headers):
    """設定Chrome選項"""
    options = webdriver.ChromeOptions()
    options.binary_location = "/opt/chrome/chrome"

    # 添加所有優化選項
    for option in ChromeOptionsBuilder.get_all_optimized_options():
        options.add_argument(option)

    # 設定視窗大小
    options.add_argument(f"--window-size={viewport['width']}x{viewport['height']}")

    # 設定臨時目錄
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    # 添加自定義標頭
    if headers:
        for key, value in headers.items():
            options.add_argument(f"--header={key}: {value}")

    return options


def _configure_driver(driver, params):
    """配置驅動程式"""
    driver.set_page_load_timeout(params["page_load_timeout"])
    driver.set_window_size(params["viewport"]["width"], params["viewport"]["height"])

    # 設定Cookies
    if params["cookies"]:
        driver.get(params["url"])
        for cookie in params["cookies"]:
            driver.add_cookie(cookie)


def _navigate_to_url(driver, url, method):
    """導航到URL"""
    print(f"🌐 正在導航到: {url}")
    start_time = time.time()

    try:
        if method == "GET":
            driver.get(url)
        else:
            driver.get(url)  # 目前只支援GET方法
        navigation_time = time.time() - start_time
        print(f"✅ 頁面導航完成 ({navigation_time:.2f}s)")
    except Exception as e:
        navigation_time = time.time() - start_time
        print(f"⚠️ 頁面導航發生問題 ({navigation_time:.2f}s): {str(e)}")
        # 繼續執行，有時候頁面仍然可以載入


def _extract_text_content(driver, selector):
    """提取文字內容"""
    try:
        if selector.startswith("//"):
            # XPath selector
            element = driver.find_element(By.XPATH, selector)
        else:
            # CSS selector
            element = driver.find_element(By.CSS_SELECTOR, selector)

        return {"text": element.text, "html": element.get_attribute("innerHTML")}
    except Exception as e:
        return {
            "text": driver.find_element(By.TAG_NAME, "body").text,
            "html": driver.page_source,
            "selector_error": str(e),
        }


def _format_response(data, is_api_gateway, status_code=200):
    """格式化回應"""
    if is_api_gateway:
        return {
            "statusCode": status_code,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(data, ensure_ascii=False),
        }
    else:
        return data
