FROM umihico/aws-lambda-selenium-python:3.12.7

# Install basic fonts that are commonly available
RUN dnf update -y && \
    dnf install -y \
    fontconfig \
    dejavu-sans-fonts \
    dejavu-serif-fonts \
    dejavu-sans-mono-fonts \
    liberation-fonts \
    && dnf clean all

# Try to install Chinese fonts - use || true to continue if some fail
RUN (dnf install -y epel-release || true) && \
    (dnf install -y google-noto-cjk-fonts || true) && \
    (dnf install -y wqy-microhei-fonts || true) && \
    (dnf install -y wqy-zenhei-fonts || true) && \
    (dnf install -y glibc-langpack-zh || true) && \
    (dnf install -y fontawesome-fonts || true) && \
    (dnf install -y open-sans-fonts || true) && \
    dnf clean all

# Create fonts directory and update font cache
RUN mkdir -p /usr/share/fonts/chinese && \
    fc-cache -fv

# Set font environment variables
ENV FONTCONFIG_PATH=/etc/fonts
ENV LANG=zh_TW.UTF-8
ENV LC_ALL=zh_TW.UTF-8

COPY *.py ./
CMD [ "main.handler" ]
