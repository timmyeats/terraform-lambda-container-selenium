"""
頁面載入策略模組
Page Loading Strategy Module
此模組負責處理現代網站的頁面載入策略
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PageLoadingStrategy:
    """頁面載入策略處理器"""

    def __init__(self, driver):
        """初始化載入策略處理器"""
        self.driver = driver

    def execute_smart_loading(self, wait_for=None, wait_timeout=3):
        """執行頁面載入策略"""
        print("🎯 現代網站頁面載入策略...")
        wait_start = time.time()

        # Strategy 1: 立即基本檢查
        page_loaded = self._check_basic_page_info()

        # Strategy 2: 頁面內容檢測
        content_loaded = self._detect_content()

        # Strategy 3: 條件性最小等待
        if not content_loaded:
            self._minimal_wait()

        # Strategy 4: 等待指定元素（如果有要求）
        if wait_for:
            self._wait_for_element(wait_for, wait_timeout)

        total_wait_time = time.time() - wait_start
        page_status = "✅" if page_loaded else "❌"
        content_status = "✅" if content_loaded else "❌"
        print(
            f"🏁 載入完成 (總耗時: {total_wait_time:.2f}s, 頁面: {page_status}, 內容: {content_status})"
        )

        return {
            "page_loaded": page_loaded,
            "content_loaded": content_loaded,
            "total_time": total_wait_time,
        }

    def _check_basic_page_info(self):
        """檢查基本頁面資訊"""
        try:
            current_url = self.driver.current_url
            page_title = self.driver.title
            print(f"🔗 頁面 URL: {current_url}")
            print(
                f"📝 頁面標題: {page_title[:50]}..." if len(page_title) > 50 else page_title
            )
            return True
        except Exception as e:
            print(f"⚠️ 頁面基本資訊無法讀取: {str(e)[:30]}...")
            return False

    def _detect_content(self):
        """頁面內容檢測"""
        try:
            content_indicators = self.driver.execute_script(
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

                # 判斷內容是否充足
                if text_len > 500 or (img_count > 3 and link_count > 5) or has_main:
                    print("✅ 內容載入充足，無需等待")
                    return True
                else:
                    print("⏳ 內容較少，進行短暫等待...")
                    return False

        except Exception as e:
            print(f"⚠️ 內容檢測失敗: {str(e)[:30]}...")
            return False

    def _minimal_wait(self):
        """最小等待策略"""
        print("⏱️ 執行最小等待策略...")
        try:
            # 短暫等待內容出現
            WebDriverWait(self.driver, 2).until(
                lambda d: len(d.find_element(By.TAG_NAME, "body").text.strip()) > 200
            )
            print("✅ 基本內容已載入")
        except Exception:
            print("⚠️ 最小等待完成，繼續處理")

        # 額外的資源等待時間
        time.sleep(1)

    def _wait_for_element(self, selector, timeout):
        """等待指定元素"""
        try:
            print(f"🎯 等待指定元素: {selector}")
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            print("✅ 指定元素已找到")
            return True
        except Exception as e:
            print(f"⚠️ 指定元素未找到，繼續執行: {str(e)[:30]}...")
            return False


class ScreenshotHandler:
    """截圖處理器"""

    def __init__(self, driver, font_handler):
        """初始化截圖處理器"""
        self.driver = driver
        self.font_handler = font_handler

    def take_screenshot(self):
        """執行截圖流程"""
        try:
            print("📸 準備截圖...")
            screenshot_start = time.time()

            # 應用截圖專用字體優化
            self.font_handler.apply_screenshot_fonts(self.driver)

            # 強制重新渲染
            self.font_handler.force_rerender(self.driver)

            # 等待字體載入和渲染
            time.sleep(2)

            # 滾動到頂部
            self._scroll_to_top()

            # 執行截圖
            print("📷 開始截圖...")
            screenshot_bytes = self.driver.get_screenshot_as_png()

            if screenshot_bytes and len(screenshot_bytes) > 0:
                screenshot_time = time.time() - screenshot_start
                print(
                    f"✅ 截圖完成！(大小: {len(screenshot_bytes)} bytes, 耗時: {screenshot_time:.2f}s)"
                )
                return {
                    "success": True,
                    "data": screenshot_bytes,
                    "size": len(screenshot_bytes),
                    "time": screenshot_time,
                }
            else:
                raise Exception("截圖數據為空")

        except Exception as e:
            print(f"❌ 截圖錯誤: {str(e)}")
            return self._fallback_screenshot(str(e))

    def _scroll_to_top(self):
        """滾動到頁面頂部"""
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            print("✅ 頁面已滾動到頂部")
        except Exception:
            print("⚠️ 無法滾動頁面")

    def _fallback_screenshot(self, error_msg):
        """備用截圖方法"""
        fallback_error = None
        try:
            print("🔄 嘗試備用截圖方法...")
            screenshot_bytes = self.driver.get_screenshot_as_png()
            if screenshot_bytes:
                print("✅ 備用截圖成功！")
                return {
                    "success": True,
                    "data": screenshot_bytes,
                    "size": len(screenshot_bytes),
                    "fallback": True,
                    "original_error": error_msg,
                }
        except Exception as e:
            fallback_error = e
            print(f"❌ 備用截圖也失敗: {fallback_error}")

        return {
            "success": False,
            "error": error_msg,
            "fallback_error": str(fallback_error) if fallback_error else None,
        }
