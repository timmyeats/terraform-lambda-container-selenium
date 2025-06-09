FROM umihico/aws-lambda-selenium-python:3.12.7

# Install Chinese fonts and font configuration tools
RUN dnf update -y && \
    dnf install -y \
    fontconfig \
    dejavu-sans-fonts \
    dejavu-serif-fonts \
    dejavu-sans-mono-fonts \
    google-noto-sans-cjk-tc-fonts \
    google-noto-serif-cjk-tc-fonts \
    google-noto-sans-tc-fonts \
    wqy-microhei-fonts \
    wqy-zenhei-fonts \
    liberation-fonts \
    glibc-langpack-zh \
    && dnf clean all

# Create fonts directory and update font cache
RUN mkdir -p /usr/share/fonts/chinese && \
    fc-cache -fv

# Set font environment variables
ENV FONTCONFIG_PATH=/etc/fonts
ENV LANG=zh_TW.UTF-8
ENV LC_ALL=zh_TW.UTF-8

COPY main.py ./
CMD [ "main.handler" ]
