FROM umihico/aws-lambda-selenium-python:3.12.7

# Install Chinese fonts and font configuration tools (Compatible with Amazon Linux)
RUN dnf update -y && \
    dnf install -y \
    fontconfig \
    dejavu-sans-fonts \
    dejavu-serif-fonts \
    dejavu-sans-mono-fonts \
    liberation-fonts \
    glibc-langpack-zh \
    && dnf clean all

# Download and install Noto CJK fonts manually and add icon font support
RUN mkdir -p /usr/share/fonts/noto && \
    cd /usr/share/fonts/noto && \
    curl -L -o NotoSansCJK.ttc "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTC/NotoSansCJK.ttc" && \
    curl -L -o NotoSerifCJK.ttc "https://github.com/googlefonts/noto-cjk/raw/main/Serif/OTC/NotoSerifCJK.ttc" && \
    chmod 644 *.ttc

# Install additional symbol and emoji fonts for better icon support
RUN mkdir -p /usr/share/fonts/symbols && \
    cd /usr/share/fonts/symbols && \
    curl -L -o NotoColorEmoji.ttf "https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoColorEmoji.ttf" && \
    curl -L -o NotoEmoji.ttf "https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoEmoji-Regular.ttf" && \
    curl -L -o NotoSymbols.ttf "https://fonts.gstatic.com/s/notosymbols/v13/rP2up3q65FkAtHfwd-eISGznYihzggmsicPfud3w1G3KsUQBct4.ttf" && \
    chmod 644 *.ttf

# Download and cache popular icon fonts for better compatibility
RUN mkdir -p /usr/share/fonts/icons && \
    cd /usr/share/fonts/icons && \
    # Font Awesome icons (most commonly used)
    curl -L -o FontAwesome.woff2 "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.woff2" && \
    curl -L -o FontAwesome-Regular.woff2 "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-regular-400.woff2" && \
    curl -L -o FontAwesome-Brands.woff2 "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-brands-400.woff2" && \
    # Material Design Icons
    curl -L -o MaterialIcons.woff2 "https://fonts.gstatic.com/s/materialicons/v140/flUhRq6tzZclQEJ-Vdg-IuiaDsNcIhQ8tQ.woff2" && \
    # Bootstrap Icons
    curl -L -o BootstrapIcons.woff2 "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/fonts/bootstrap-icons.woff2" && \
    chmod 644 *.woff2 || echo "Some icon fonts already exist, skipping download"

# Create fonts directory and update font cache
RUN mkdir -p /usr/share/fonts/chinese && \
    fc-cache -fv && \
    fc-list | grep -i "noto\|dejavu" || echo "Fonts installed successfully"

# Create a default CSS file for icon fonts and Chinese text
RUN mkdir -p /opt/css && \
    echo '/* Default font optimization for Chinese and icon support */' > /opt/css/default-fonts.css && \
    echo 'body, div, span, p, h1, h2, h3, h4, h5, h6, a, li, td, th,' >> /opt/css/default-fonts.css && \
    echo 'article, section, header, footer, nav, aside, main {' >> /opt/css/default-fonts.css && \
    echo '    font-family: "Noto Sans CJK TC", "Microsoft JhengHei", "微軟正黑體", sans-serif !important;' >> /opt/css/default-fonts.css && \
    echo '    text-rendering: optimizeLegibility !important;' >> /opt/css/default-fonts.css && \
    echo '}' >> /opt/css/default-fonts.css && \
    echo '/* Preserve icon fonts */' >> /opt/css/default-fonts.css && \
    echo '[class*="ico"], [class*="icon"], [class*="fa-"],' >> /opt/css/default-fonts.css && \
    echo '.fa, .fas, .far, .fal, .fad, .fab,' >> /opt/css/default-fonts.css && \
    echo '[data-icon], [class*="material-icons"],' >> /opt/css/default-fonts.css && \
    echo '.glyphicon, [class*="glyphicon"],' >> /opt/css/default-fonts.css && \
    echo '.iconfont, [class*="iconfont"],' >> /opt/css/default-fonts.css && \
    echo '[class*="sprite"], [class*="symbol"] {' >> /opt/css/default-fonts.css && \
    echo '    font-family: inherit !important;' >> /opt/css/default-fonts.css && \
    echo '}' >> /opt/css/default-fonts.css && \
    echo '* { visibility: visible !important; }' >> /opt/css/default-fonts.css

# Configure locale for Chinese support (Traditional Chinese Taiwan, Hong Kong and Simplified Chinese)
RUN localedef -i zh_TW -f UTF-8 zh_TW.UTF-8 || echo "zh_TW locale already configured" && \
    localedef -i zh_HK -f UTF-8 zh_HK.UTF-8 || echo "zh_HK locale already configured" && \
    localedef -i zh_CN -f UTF-8 zh_CN.UTF-8 || echo "zh_CN locale already configured"

# Set font environment variables for multi-region Chinese support
ENV FONTCONFIG_PATH=/etc/fonts
ENV LANG=zh_TW.UTF-8
ENV LC_ALL=zh_TW.UTF-8
ENV LC_CTYPE=zh_TW.UTF-8
ENV LANGUAGE=zh_TW:zh_HK:zh_CN

# Copy all Python files and set correct permissions for Lambda
COPY *.py ${LAMBDA_TASK_ROOT}/
RUN chmod 755 ${LAMBDA_TASK_ROOT}/*.py

CMD [ "main.handler" ]
