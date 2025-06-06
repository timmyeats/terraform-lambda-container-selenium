"""
字體處理模組
Font Handler Module
此模組負責處理字體的優化和圖示字體的保留
"""


class ChineseFontHandler:
    """中文字體處理器"""

    def __init__(self):
        """初始化字體處理器"""
        self.google_fonts_url = (
            "https://fonts.googleapis.com/css2?"
            "family=Noto+Sans+TC:wght@300;400;500;700&"
            "family=Noto+Serif+TC:wght@300;400;500;700&"
            "display=swap"
        )
        self.default_css_path = "/opt/css/default-fonts.css"

    def get_basic_font_css(self):
        """獲取基本中文字體CSS"""
        return """
            body, div, span, p, h1, h2, h3, h4, h5, h6, a, li, td, th,
            article, section, header, footer, nav, aside, main,
            .title, .content, .text, .news, .article {
                font-family: 'Noto Sans TC', 'Noto Sans CJK TC', 'Microsoft JhengHei',
                            '微軟正黑體', 'PingFang TC', 'Helvetica Neue', Arial, sans-serif !important;
                text-rendering: optimizeLegibility !important;
                -webkit-font-smoothing: antialiased !important;
                -moz-osx-font-smoothing: grayscale !important;
            }

            /* 保留圖示字體 - 基礎版本 */
            [class*="ico"], [class*="icon"], [class*="fa-"],
            .fa, .fas, .far, .fal, .fad, .fab,
            [data-icon], [class*="material-icons"],
            .glyphicon, [class*="glyphicon"],
            .iconfont, [class*="iconfont"],
            select, .select, [class*="select"],
            .dropdown, [class*="dropdown"], [class*="arrow"], [class*="chevron"] {
                font-family: inherit !important;
            }

            /* 保留偽元素圖示 - 基礎版本 */
            [class*="ico"]::before, [class*="ico"]::after,
            [class*="icon"]::before, [class*="icon"]::after,
            [class*="fa-"]::before, [class*="fa-"]::after,
            .fa::before, .fa::after, .fas::before, .fas::after,
            select::before, select::after,
            .dropdown::before, .dropdown::after,
            [class*="arrow"]::before, [class*="arrow"]::after {
                font-family: inherit !important;
            }

            * { visibility: visible !important; }
        """

    def get_enhanced_font_css(self):
        """獲取增強版中文字體CSS，包含Google Fonts導入"""
        return f"""
            @import url('{self.google_fonts_url}');

            /* 中文字體優化 */
            body, div, span, p, h1, h2, h3, h4, h5, h6, a, li, td, th,
            article, section, header, footer, nav, aside, main,
            .title, .content, .text, .news, .article {{
                font-family: 'Noto Sans TC', 'Noto Sans CJK TC', 'Microsoft JhengHei',
                            '微軟正黑體', 'PingFang TC', 'Helvetica Neue', Arial, sans-serif !important;
                text-rendering: optimizeLegibility !important;
                -webkit-font-smoothing: antialiased !important;
                -moz-osx-font-smoothing: grayscale !important;
            }}

            /* 保留圖示字體 - 增強版本 */
            [class*="ico"], [class*="icon"], [class*="fa-"],
            .fa, .fas, .far, .fal, .fad, .fab, .fass, .fasr, .fasl,
            [data-icon], [class*="material-icons"], [class*="material-symbols"],
            .glyphicon, [class*="glyphicon"],
            .iconfont, [class*="iconfont"],
            [class*="sprite"], [class*="symbol"],
            select, .select, [class*="select"],
            .dropdown, [class*="dropdown"], [class*="arrow"], [class*="chevron"], [class*="caret"],
            .nav, [class*="nav"], [class*="menu"] {{
                font-family: inherit !important;
            }}

            /* 保留偽元素圖示 - 增強版本 */
            [class*="ico"]::before, [class*="ico"]::after,
            [class*="icon"]::before, [class*="icon"]::after,
            [class*="fa-"]::before, [class*="fa-"]::after,
            .fa::before, .fa::after, .fas::before, .fas::after,
            .far::before, .far::after, .fal::before, .fal::after,
            .fad::before, .fad::after, .fab::before, .fab::after,
            select::before, select::after,
            .dropdown::before, .dropdown::after,
            [class*="arrow"]::before, [class*="arrow"]::after,
            [class*="chevron"]::before, [class*="chevron"]::after {{
                font-family: inherit !important;
            }}

            * {{ visibility: visible !important; }}
        """

    def get_screenshot_font_css(self):
        """獲取截圖專用的字體CSS，包含完整的圖示字體保留"""
        return f"""
            @import url('{self.google_fonts_url}');

            /* 中文字體優化 */
            body, div, span, p, h1, h2, h3, h4, h5, h6, a, li, td, th,
            article, section, header, footer, nav, aside, main,
            .title, .content, .text, .news, .article {{
                font-family: 'Noto Sans TC', 'Noto Sans CJK TC', 'Microsoft JhengHei',
                            '微軟正黑體', 'PingFang TC', sans-serif !important;
                text-rendering: optimizeLegibility !important;
                -webkit-font-smoothing: antialiased !important;
                -moz-osx-font-smoothing: grayscale !important;
            }}

            /* 保留圖示字體 - 基礎類別 */
            [class*="ico"], [class*="icon"], [class*="fa-"],
            .fa, .fas, .far, .fal, .fad, .fab, .fass, .fasr, .fasl,
            [data-icon], [class*="material-icons"], [class*="material-symbols"],
            .glyphicon, [class*="glyphicon"],
            .iconfont, [class*="iconfont"],
            [class*="sprite"], [class*="symbol"],
            [class*="glyph"], [class*="pictogram"] {{
                font-family: inherit !important;
            }}

            /* 保留下拉選單和導航圖示 */
            select, .select, [class*="select"],
            .dropdown, [class*="dropdown"], [class*="drop-down"],
            .combobox, [class*="combo"],
            [class*="arrow"], [class*="chevron"], [class*="caret"],
            .nav, [class*="nav"], [class*="menu"],
            .btn, [class*="btn"], [class*="button"],
            [role="combobox"], [role="listbox"], [role="menu"],
            [aria-haspopup], [class*="popup"] {{
                font-family: inherit !important;
            }}

            /* 保留偽元素圖示 - 基礎類別 */
            [class*="ico"]::before, [class*="ico"]::after,
            [class*="icon"]::before, [class*="icon"]::after,
            [class*="fa-"]::before, [class*="fa-"]::after,
            .fa::before, .fa::after, .fas::before, .fas::after,
            .far::before, .far::after, .fal::before, .fal::after,
            .fad::before, .fad::after, .fab::before, .fab::after,
            .fass::before, .fass::after, .fasr::before, .fasr::after,
            .fasl::before, .fasl::after {{
                font-family: inherit !important;
            }}

            /* 保留下拉選單和導航偽元素 */
            select::before, select::after,
            .select::before, .select::after, [class*="select"]::before, [class*="select"]::after,
            .dropdown::before, .dropdown::after, [class*="dropdown"]::before, [class*="dropdown"]::after,
            [class*="arrow"]::before, [class*="arrow"]::after,
            [class*="chevron"]::before, [class*="chevron"]::after,
            [class*="caret"]::before, [class*="caret"]::after,
            .nav::before, .nav::after, [class*="nav"]::before, [class*="nav"]::after,
            [class*="menu"]::before, [class*="menu"]::after,
            .btn::before, .btn::after, [class*="btn"]::before, [class*="btn"]::after {{
                font-family: inherit !important;
            }}

            /* 特殊圖示字體系統保留 */
            [style*="font-family"][style*="icon"],
            [style*="font-family"][style*="fa-"],
            [style*="font-family"][style*="material"],
            [style*="font-family"][style*="glyph"],
            [class*="webfont"], [class*="font-icon"] {{
                font-family: inherit !important;
            }}

            /* 確保文字可見性 */
            * {{ visibility: visible !important; }}
        """

    def apply_basic_fonts(self, driver):
        """應用基本中文字體優化"""
        try:
            print("🔤 應用基本中文字體優化...")

            # 嘗試使用預設CSS檔案
            try:
                with open(self.default_css_path, "r") as f:
                    css_content = f.read()
                driver.execute_script(
                    f"""
                    const style = document.createElement('style');
                    style.setAttribute('data-font-basic', 'true');
                    style.textContent = `{css_content}`;
                    document.head.appendChild(style);
                """
                )
                print("✅ 使用預設CSS檔案成功")
                return True
            except Exception as file_error:
                print(f"⚠️ 預設CSS檔案讀取失敗: {file_error}")

                # 使用內建CSS作為備用方案
                css_content = self.get_basic_font_css()
                driver.execute_script(
                    f"""
                    const style = document.createElement('style');
                    style.setAttribute('data-font-basic', 'true');
                    style.textContent = `{css_content}`;
                    document.head.appendChild(style);
                """
                )
                print("✅ 使用內建CSS成功")
                return True

        except Exception as e:
            print(f"❌ 基本字體優化失敗: {e}")
            return False

    def apply_enhanced_fonts(self, driver):
        """應用增強版中文字體優化，包含Google Fonts"""
        try:
            print("🔤 應用增強中文字體支援...")
            driver.execute_script(
                f"""
                // Remove any existing font styles first
                const existingStyles = document.querySelectorAll(
                    'style[data-font-fix], style[data-font-basic], style[data-font-enhanced]'
                );
                existingStyles.forEach(style => style.remove());

                // Inject Google Fonts for better Chinese support
                if (!document.querySelector('link[href*="fonts.googleapis.com"]')) {{
                    const googleFonts = document.createElement('link');
                    googleFonts.rel = 'stylesheet';
                    googleFonts.href = '{self.google_fonts_url}';
                    document.head.appendChild(googleFonts);
                }}

                // Apply comprehensive Chinese font CSS
                const style = document.createElement('style');
                style.setAttribute('data-font-enhanced', 'true');
                style.textContent = `{self.get_enhanced_font_css()}`;
                document.head.appendChild(style);
            """
            )
            print("✅ 增強中文字體支援完成")
            return True
        except Exception as e:
            print(f"⚠️ 增強字體支援失敗，使用基本方案: {e}")
            return self.apply_basic_fonts(driver)

    def apply_screenshot_fonts(self, driver):
        """應用截圖專用字體優化"""
        try:
            print("🎨 注入截圖專用字體優化...")
            driver.execute_script(
                f"""
                // Remove any existing font styles first
                const existingFontStyles = document.querySelectorAll(
                    'style[data-font-fix], style[data-screenshot-fonts]'
                );
                existingFontStyles.forEach(style => style.remove());

                // Inject Google Fonts for better rendering
                if (!document.querySelector('link[href*="fonts.googleapis.com"]')) {{
                    const googleFonts = document.createElement('link');
                    googleFonts.rel = 'stylesheet';
                    googleFonts.href = '{self.google_fonts_url}';
                    document.head.appendChild(googleFonts);
                }}

                // Inject optimized font styles
                const style = document.createElement('style');
                style.setAttribute('data-font-fix', 'true');
                style.textContent = `{self.get_screenshot_font_css()}`;
                document.head.appendChild(style);
                document.body.offsetHeight; // Force reflow
            """
            )
            print("✅ 截圖字體優化完成")
            return True
        except Exception as e:
            print(f"⚠️ 截圖字體優化失敗: {e}")
            return False

    def force_rerender(self, driver):
        """強制重新渲染頁面"""
        try:
            driver.execute_script(
                """
                // Force browser to re-render with new fonts
                document.body.style.display = 'none';
                document.body.offsetHeight; // Trigger reflow
                document.body.style.display = '';
            """
            )
            print("✅ 強制重新渲染完成")
            return True
        except Exception as e:
            print(f"⚠️ 重新渲染失敗: {e}")
            return False


class ChromeOptionsBuilder:
    """Chrome選項建構器"""

    @staticmethod
    def get_base_options():
        """獲取基本Chrome選項"""
        return [
            "--headless",
            "--no-sandbox",
            "--disable-gpu",
            "--single-process",
            "--disable-dev-shm-usage",
            "--disable-dev-tools",
            "--no-zygote",
        ]

    @staticmethod
    def get_performance_options():
        """獲取性能優化選項"""
        return [
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            "--disable-ipc-flooding-protection",
            "--disable-hang-monitor",
            "--disable-prompt-on-repost",
            "--disable-background-networking",
            "--disable-sync",
            "--metrics-recording-only",
            "--no-first-run",
        ]

    @staticmethod
    def get_font_options():
        """獲取字體渲染優化選項"""
        return [
            "--lang=zh-TW",
            "--enable-font-antialiasing",
            "--force-device-scale-factor=1",
            "--font-render-hinting=full",
            "--enable-lcd-text",
            "--disable-font-subpixel-positioning",
        ]

    @staticmethod
    def get_network_options():
        """獲取網路優化選項"""
        return [
            "--aggressive-cache-discard",
            "--disable-extensions",
            "--disable-plugins",
            "--allow-running-insecure-content",
        ]

    @staticmethod
    def get_all_optimized_options():
        """獲取所有優化選項"""
        options = []
        options.extend(ChromeOptionsBuilder.get_base_options())
        options.extend(ChromeOptionsBuilder.get_performance_options())
        options.extend(ChromeOptionsBuilder.get_font_options())
        options.extend(ChromeOptionsBuilder.get_network_options())
        return options
