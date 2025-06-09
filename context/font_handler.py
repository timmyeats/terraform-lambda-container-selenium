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
                font-family: 'Font Awesome 5 Free', 'Font Awesome 5 Pro', 'Font Awesome 6 Free', 'Font Awesome 6 Pro',
                            'Material Icons', 'Material Symbols Outlined', 'iconfont',
                            -webkit-pictograph, serif !important;
            }

            /* 保留偽元素圖示 - 基礎版本 */
            [class*="ico"]::before, [class*="ico"]::after,
            [class*="icon"]::before, [class*="icon"]::after,
            [class*="fa-"]::before, [class*="fa-"]::after,
            .fa::before, .fa::after, .fas::before, .fas::after,
            select::before, select::after,
            .dropdown::before, .dropdown::after,
            [class*="arrow"]::before, [class*="arrow"]::after {
                font-family: 'Font Awesome 5 Free', 'Font Awesome 5 Pro', 'Font Awesome 6 Free', 'Font Awesome 6 Pro',
                            'Material Icons', 'Material Symbols Outlined', 'iconfont',
                            -webkit-pictograph, serif !important;
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
                font-family: 'Font Awesome 5 Free', 'Font Awesome 5 Pro', 'Font Awesome 6 Free', 'Font Awesome 6 Pro',
                            'Material Icons', 'Material Symbols Outlined', 'iconfont',
                            -webkit-pictograph, serif !important;
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
                font-family: 'Font Awesome 5 Free', 'Font Awesome 5 Pro', 'Font Awesome 6 Free', 'Font Awesome 6 Pro',
                            'Material Icons', 'Material Symbols Outlined', 'iconfont',
                            -webkit-pictograph, serif !important;
            }}

            * {{ visibility: visible !important; }}
        """

    def get_screenshot_font_css(self):
        """獲取截圖專用的字體CSS，排除圖示類別避免干擾"""
        return f"""
            @import url('{self.google_fonts_url}');

            /* 中文字體優化 - 排除圖示類別 */
            body, div, span, p, h1, h2, h3, h4, h5, h6, a, li, td, th,
            article, section, header, footer, nav, aside, main,
            .title, .content, .text, .news, .article,
            /* 特定排除圖示類別 */
            :not([class*="ico"]):not([class*="icon"]):not([class*="fa-"]):not(.fa):not(.fas):not(.far):not(.fal):not(.fad):not(.fab) {{
                font-family: 'Noto Sans TC', 'Noto Sans CJK TC', 'Microsoft JhengHei',
                            '微軟正黑體', 'PingFang TC', sans-serif !important;
                text-rendering: optimizeLegibility !important;
                -webkit-font-smoothing: antialiased !important;
                -moz-osx-font-smoothing: grayscale !important;
            }}

            /* 確保文字可見性，但排除圖示 */
            :not([class*="ico"]):not([class*="icon"]):not([class*="fa-"]):not(.fa):not(.fas):not(.far):not(.fal):not(.fad):not(.fab) {{
                visibility: visible !important;
            }}
        """

    def get_icon_fix_css(self):
        """獲取專門修復圖示顯示問題的CSS - 使用排除策略"""
        return """
            /* 🎯 新策略：完全不碰圖示，只確保基本顯示屬性 */
            .ico, [class*="ico"], .icon, [class*="icon"],
            [class^="fa-"], [class*=" fa-"], .fa, .fas, .far, .fal, .fad, .fab {
                /* 只設定顯示相關屬性，不碰字體 */
                display: inline-block !important;
                visibility: visible !important;
                opacity: 1 !important;
                /* 清理可能影響的屬性 */
                text-indent: 0 !important;
                letter-spacing: normal !important;
                word-spacing: normal !important;
                text-decoration: none !important;
            }

            /* 🔧 偽元素：只確保顯示，不改變任何字體相關屬性 */
            .ico::before, .ico::after, [class*="ico"]::before, [class*="ico"]::after,
            .icon::before, .icon::after, [class*="icon"]::before, [class*="icon"]::after,
            [class^="fa-"]::before, [class*=" fa-"]::before, [class^="fa-"]::after, [class*=" fa-"]::after,
            .fa::before, .fa::after, .fas::before, .fas::after, .far::before, .far::after,
            .fal::before, .fal::after, .fad::before, .fad::after, .fab::before, .fab::after {
                /* 只確保偽元素可見，其他都不碰 */
                display: inline-block !important;
                visibility: visible !important;
                opacity: 1 !important;
                text-decoration: none !important;
            }

            /* 🎯 針對導航選單圖示 - 最小干預 */
            .masthead__nav-link .ico,
            .masthead__nav-item .ico,
            .masthead__nav .ico {
                display: inline-block !important;
                visibility: visible !important;
                opacity: 1 !important;
            }

            .masthead__nav-link .ico::before,
            .masthead__nav-item .ico::before,
            .masthead__nav .ico::before {
                display: inline-block !important;
                visibility: visible !important;
                opacity: 1 !important;
            }
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
                    'style[data-font-fix], style[data-screenshot-fonts], style[data-icon-fix]'
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

                // Inject icon fix styles
                const iconStyle = document.createElement('style');
                iconStyle.setAttribute('data-icon-fix', 'true');
                iconStyle.textContent = `{self.get_icon_fix_css()}`;
                document.head.appendChild(iconStyle);

                document.body.offsetHeight; // Force reflow
            """
            )
            print("✅ 截圖字體優化完成")
            print("🎯 圖示修復CSS已注入")
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
        """獲取字體渲染優化選項（不包含語系設定）"""
        return [
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
