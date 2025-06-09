import json
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tempfile import mkdtemp
import time
from font_handler import ChineseFontHandler  # noqa: F401
from loading_handler import PageLoadingStrategy, ScreenshotHandler  # noqa: F401


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
        wait_timeout = payload.get("wait_timeout", 5)  # Further reduced timeout
        page_load_timeout = payload.get(
            "page_load_timeout", 15
        )  # Further reduced timeout
        viewport = payload.get("viewport", {"width": 1600, "height": 900})
        headers = payload.get("headers", {})
        cookies = payload.get("cookies", [])
        form_data = payload.get("form_data", {})

        # Setup Chrome options with modern website optimizations
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

        # Performance and stability optimizations for modern websites
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-prompt-on-repost")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-sync")
        options.add_argument("--metrics-recording-only")
        options.add_argument("--no-first-run")

        # Networking and loading optimizations
        options.add_argument("--aggressive-cache-discard")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        # Note: Keep JavaScript enabled for modern websites
        # options.add_argument("--disable-web-security")  # For easier content access
        options.add_argument("--allow-running-insecure-content")

        # Enhanced font and rendering for Chinese content
        options.add_argument("--font-render-hinting=none")
        options.add_argument("--disable-font-subpixel-positioning")
        options.add_argument("--lang=zh-TW")
        options.add_argument("--enable-font-antialiasing")
        options.add_argument("--disable-lcd-text")
        options.add_argument("--force-device-scale-factor=1")

        # Font configuration for Chinese characters
        options.add_argument("--enable-features=FontAccessAPI")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-site-isolation-trials")

        # Create temporary directories
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
            # Set page load timeout
            driver.set_page_load_timeout(page_load_timeout)

            # Set viewport size
            driver.set_window_size(viewport["width"], viewport["height"])

            # Add cookies if provided
            if cookies:
                # Navigate to domain first to set cookies
                driver.get(url)
                for cookie in cookies:
                    driver.add_cookie(cookie)

            # Navigate to URL
            print(f"🌐 正在導航到: {url}")
            start_time = time.time()

            try:
                if method == "GET":
                    driver.get(url)
                else:
                    driver.get(url)
                navigation_time = time.time() - start_time
                print(f"✅ 頁面導航完成 ({navigation_time:.2f}s)")
            except Exception as e:
                navigation_time = time.time() - start_time
                print(f"⚠️ 頁面導航發生問題 ({navigation_time:.2f}s): {str(e)}")
                # 繼續執行，有時候頁面仍然可以載入

            # Modern website loading strategy - optimized for news sites like AM730
            print("🎯 現代網站智能載入策略...")
            wait_start = time.time()

            # Strategy 1: Immediate basic check
            page_loaded = False
            content_loaded = False

            try:
                # Check if we can access basic page properties
                current_url = driver.current_url
                page_title = driver.title
                print(f"🔗 頁面 URL: {current_url}")
                print(
                    f"📝 頁面標題: {page_title[:50]}..."
                    if len(page_title) > 50
                    else page_title
                )
                page_loaded = True
            except Exception as e:
                print(f"⚠️ 頁面基本資訊無法讀取: {str(e)[:30]}...")

            # Strategy 2: Smart content detection (don't wait for full document.readyState)
            try:
                # Look for actual content rather than just document ready
                content_indicators = driver.execute_script(
                    """
                    const body = document.body;
                    const textLength = body ? body.textContent.length : 0;
                    const imageCount = document.querySelectorAll('img').length;
                    const linkCount = document.querySelectorAll('a').length;
                    const hasMainContent = !!(
                        document.querySelector('main') ||
                        document.querySelector('[class*="content"]') ||
                        document.querySelector('article') ||
                        document.querySelector('.news') ||
                        document.querySelector('#content')
                    );

                    return {
                        textLength: textLength,
                        imageCount: imageCount,
                        linkCount: linkCount,
                        hasMainContent: hasMainContent,
                        readyState: document.readyState
                    };
                """
                )

                if content_indicators:
                    text_len = content_indicators.get("textLength", 0)
                    img_count = content_indicators.get("imageCount", 0)
                    link_count = content_indicators.get("linkCount", 0)
                    has_main = content_indicators.get("hasMainContent", False)
                    ready_state = content_indicators.get("readyState", "unknown")

                    print(f"📊 內容分析: 文字{text_len}字符, {img_count}張圖片, {link_count}個連結")
                    print(f"🏗️ 狀態: {ready_state}, 主要內容: {'✅' if has_main else '❌'}")

                    # Consider content loaded if we have reasonable amount of content
                    if text_len > 500 or (img_count > 3 and link_count > 5) or has_main:
                        content_loaded = True
                        print("✅ 內容載入充足，無需等待")
                    else:
                        print("⏳ 內容較少，進行短暫等待...")

            except Exception as e:
                print(f"⚠️ 內容檢測失敗: {str(e)[:30]}...")

            # Strategy 3: Conditional minimal waiting
            if not content_loaded:
                print("⏱️ 執行最小等待策略...")
                try:
                    # Very short wait for content to appear
                    WebDriverWait(driver, 2).until(
                        lambda d: len(d.find_element(By.TAG_NAME, "body").text.strip())
                        > 200
                    )
                    print("✅ 基本內容已載入")
                except Exception as e:
                    print(f"⚠️ 最小等待完成，繼續處理: {str(e)}")

                # Additional short wait for resources
                time.sleep(1)

            # Strategy 4: Wait for specific element only if explicitly requested
            if wait_for:
                try:
                    print(f"🎯 等待指定元素: {wait_for}")
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, wait_for))
                    )
                    print("✅ 指定元素已找到")
                except Exception as e:
                    print(f"⚠️ 指定元素未找到，繼續執行: {str(e)[:30]}...")

            total_wait_time = time.time() - wait_start
            print(
                f"🏁 載入策略完成 (總耗時: {total_wait_time:.2f}s, 頁面: {'✅' if page_loaded else '❌'}, 內容: {'✅' if content_loaded else '❌'})"
            )

            # Early font enhancement - apply immediately after page load
            try:
                print("🔤 頁面載入後立即優化字體...")
                driver.execute_script(
                    """
                    // Step 1: Add Google Fonts if not present
                    if (!document.querySelector('link[href*="fonts.googleapis.com"]')) {
                        const link = document.createElement('link');
                        link.rel = 'stylesheet';
                        link.href = 'https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Noto+Serif+TC:wght@400;700&display=swap';
                        document.head.appendChild(link);
                    }

                    // Step 2: Apply basic font CSS immediately
                    const quickStyle = document.createElement('style');
                    quickStyle.setAttribute('data-quick-font', 'true');
                    quickStyle.textContent = `
                        * {
                            font-family: 'Noto Sans TC', 'Microsoft JhengHei', '微軟正黑體', sans-serif !important;
                            text-rendering: optimizeLegibility !important;
                        }
                    `;
                    document.head.appendChild(quickStyle);
                """
                )
                print("✅ 早期字體優化完成")
            except Exception as early_font_error:
                print(f"⚠️ 早期字體優化失敗: {early_font_error}")

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
                    print("📸 準備截圖...")
                    screenshot_start = time.time()

                    # Step 1: Inject Google Fonts for Chinese support
                    try:
                        print("🔤 注入 Google Fonts 中文字體...")
                        driver.execute_script(
                            """
                            // Add Google Fonts link if not already present
                            if (!document.querySelector('link[href*="fonts.googleapis.com"]')) {
                                const link = document.createElement('link');
                                link.rel = 'stylesheet';
                                link.href = 'https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Noto+Serif+TC:wght@400;700&display=swap';
                                document.head.appendChild(link);
                                console.log('Google Fonts 已加載');
                            }
                        """
                        )

                        # Wait a moment for font loading
                        time.sleep(1.5)
                        print("✅ Google Fonts 已注入")
                    except Exception as font_error:
                        print(f"⚠️ Google Fonts 注入失敗: {font_error}")

                    # Step 2: Enhanced CSS injection for Chinese font support
                    try:
                        print("🎨 注入強化中文字體 CSS...")
                        driver.execute_script(
                            """
                            // Remove any existing font styles first
                            const existingFontStyles = document.querySelectorAll('style[data-font-fix]');
                            existingFontStyles.forEach(style => style.remove());

                            // Inject comprehensive font styles with icon protection
                            const style = document.createElement('style');
                            style.setAttribute('data-font-fix', 'true');
                            style.textContent = `
                                /* 重置文字元素的字體，但保護圖示元素 */
                                body, div, span, p, h1, h2, h3, h4, h5, h6, a, li, td, th,
                                article, section, header, footer, nav, aside, main,
                                .title, .content, .text, .news, .article {
                                    font-family: 'Noto Sans TC', 'Noto Sans CJK TC', 'Microsoft JhengHei', '微軟正黑體', 'PingFang TC', 'Apple LiGothic', 'Hiragino Sans GB', 'WenQuanYi Micro Hei', SimSun, sans-serif !important;
                                    text-rendering: optimizeLegibility !important;
                                    -webkit-font-smoothing: antialiased !important;
                                    -moz-osx-font-smoothing: grayscale !important;
                                    font-display: swap !important;
                                }

                                /* 🎯 關鍵：保護圖示元素，不覆蓋其 font-family */
                                .ico, [class*="ico"], .icon, [class*="icon"],
                                [class^="fa-"], [class*=" fa-"], .fa, .fas, .far, .fal, .fad, .fab {
                                    /* 不設定 font-family，讓原始 CSS 生效 */
                                    font-style: normal !important;
                                    font-weight: normal !important;
                                    font-variant: normal !important;
                                    text-transform: none !important;
                                    line-height: 1 !important;
                                    speak: none !important;
                                    display: inline-block !important;
                                    visibility: visible !important;
                                    opacity: 1 !important;
                                    -webkit-font-smoothing: antialiased !important;
                                    -moz-osx-font-smoothing: grayscale !important;
                                }

                                /* 🔧 保護偽元素圖示 */
                                .ico::before, .ico::after, [class*="ico"]::before, [class*="ico"]::after,
                                .icon::before, .icon::after, [class*="icon"]::before, [class*="icon"]::after,
                                [class^="fa-"]::before, [class*=" fa-"]::before,
                                .fa::before, .fa::after, .fas::before, .fas::after, .far::before, .far::after {
                                    /* 保持原始 font-family 和 content */
                                    font-style: normal !important;
                                    font-weight: normal !important;
                                    font-variant: normal !important;
                                    text-transform: none !important;
                                    line-height: 1 !important;
                                    display: inline-block !important;
                                    visibility: visible !important;
                                    opacity: 1 !important;
                                    -webkit-font-smoothing: antialiased !important;
                                    -moz-osx-font-smoothing: grayscale !important;
                                }

                                /* 🎯 特別保護 ico-thin-down */
                                .ico-thin-down, .ico.ico-thin-down {
                                    display: inline-block !important;
                                    visibility: visible !important;
                                    opacity: 1 !important;
                                    font-style: normal !important;
                                    font-variant: normal !important;
                                    line-height: 1 !important;
                                }

                                .ico-thin-down::before, .ico.ico-thin-down::before {
                                    display: inline-block !important;
                                    visibility: visible !important;
                                    opacity: 1 !important;
                                    font-style: normal !important;
                                    font-variant: normal !important;
                                    line-height: 1 !important;
                                }

                                /* 強制覆蓋可能的內聯樣式，但排除圖示 */
                                [style*="font-family"]:not(.ico):not([class*="ico"]):not(.icon):not([class*="icon"]):not([class^="fa-"]):not([class*=" fa-"]) {
                                    font-family: 'Noto Sans TC', 'Noto Sans CJK TC', 'Microsoft JhengHei', '微軟正黑體', 'PingFang TC', 'Apple LiGothic', sans-serif !important;
                                }

                                /* 確保一般文字可見性 */
                                body, div, span, p, h1, h2, h3, h4, h5, h6, a, li, td, th {
                                    color: inherit !important;
                                    visibility: visible !important;
                                }
                            `;
                            document.head.appendChild(style);

                            // Force reflow to apply styles immediately
                            document.body.offsetHeight;

                            // Log font information for debugging
                            const computedStyle = window.getComputedStyle(document.body);
                            console.log('Applied font-family:', computedStyle.fontFamily);

                            // Check icon elements
                            const iconElements = document.querySelectorAll('.ico');
                            iconElements.forEach((icon, index) => {
                                const iconStyle = window.getComputedStyle(icon);
                                console.log(`Icon ${index} font-family:`, iconStyle.fontFamily);
                                console.log(`Icon ${index} content:`, window.getComputedStyle(icon, '::before').content);
                            });

                            return {
                                appliedFont: computedStyle.fontFamily,
                                stylesApplied: true,
                                iconCount: iconElements.length
                            };
                        """
                        )
                        print("✅ 增強中文字體 CSS 已注入")
                    except Exception as css_error:
                        print(f"⚠️ CSS 注入失敗: {css_error}")

                    # Step 3: Force font re-rendering
                    try:
                        print("🔄 強制字體重新渲染...")
                        driver.execute_script(
                            """
                            // Force all text elements to re-render
                            const textElements = document.querySelectorAll('*');
                            textElements.forEach(el => {
                                if (el.textContent && el.textContent.trim()) {
                                    const originalDisplay = el.style.display;
                                    el.style.display = 'none';
                                    el.offsetHeight; // Trigger reflow
                                    el.style.display = originalDisplay;
                                }
                            });

                            // Additional font loading check
                            if (document.fonts && document.fonts.ready) {
                                return document.fonts.ready.then(() => {
                                    console.log('字體載入完成');
                                    return true;
                                });
                            }
                            return true;
                        """
                        )
                        print("✅ 字體重新渲染完成")
                    except Exception as render_error:
                        print(f"⚠️ 字體重新渲染失敗: {render_error}")

                    # Step 4: Extended wait for font rendering
                    print("⏳ 等待字體完全載入和渲染...")
                    time.sleep(2)  # Increased wait time for better font loading

                    # Scroll to top to ensure we capture from the beginning
                    try:
                        driver.execute_script("window.scrollTo(0, 0);")
                        print("✅ 頁面已滾動到頂部")
                    except Exception as e:
                        print(f"⚠️ 無法滾動頁面: {str(e)}")

                    print("📷 開始截圖...")
                    screenshot_bytes = driver.get_screenshot_as_png()

                    if screenshot_bytes and len(screenshot_bytes) > 0:
                        screenshot_b64 = base64.b64encode(screenshot_bytes).decode(
                            "utf-8"
                        )
                        response["screenshot"] = screenshot_b64
                        response["screenshot_format"] = "png"
                        response["screenshot_size"] = len(screenshot_bytes)

                        screenshot_time = time.time() - screenshot_start
                        print(
                            f"✅ 截圖完成！(大小: {len(screenshot_bytes)} bytes, 耗時: {screenshot_time:.2f}s)"
                        )
                    else:
                        raise Exception("截圖數據為空")

                except Exception as e:
                    print(f"❌ 截圖錯誤: {str(e)}")
                    response["screenshot_error"] = str(e)

                    # Try fallback screenshot without CSS injection
                    try:
                        print("🔄 嘗試備用截圖方法...")
                        screenshot_bytes = driver.get_screenshot_as_png()
                        if screenshot_bytes:
                            screenshot_b64 = base64.b64encode(screenshot_bytes).decode(
                                "utf-8"
                            )
                            response["screenshot"] = screenshot_b64
                            response["screenshot_format"] = "png"
                            response["fallback_screenshot"] = True
                            print("✅ 備用截圖成功！")
                    except Exception as fallback_error:
                        print(f"❌ 備用截圖也失敗: {fallback_error}")

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
