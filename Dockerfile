FROM python:3.8-alpine AS prod
MAINTAINER usharerose

RUN apk update && \
    apk add --no-cache tzdata bash vim curl && \
    apk upgrade && \
    rm -rf /var/cache/apk/*

# Setup base folder
RUN addgroup -S -g 1000 swish && \
    adduser -S -G swish -u 1000 swish && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    mkdir -p /home/swish/.ssh && \
    mkdir -p /services/swish/ && \
    mkdir -p /var/run/swish/gunicorn/ && \
    mkdir -p /var/log/swish/ && \
    mkdir -p /var/log/gunicorn/ && \
    chown -R root:swish /services/swish/ && \
    chown -R root:swish /var/run/swish/ && \
    chown -R swish:swish /home/swish/ && \
    chmod -R 770 /var/log/gunicorn/ && \
    chmod -R 770 /var/log/swish/ && \
    chmod -R 770 /var/run/swish/ && \
    chmod -R 750 /home/swish/ && \
    chmod -R 750 /services/swish/

# Set workdir
WORKDIR /services/swish/swish-scrape/

COPY scripts/build.sh requirements.txt ./

# Execute build script
RUN chmod +x ./build.sh && \
    ./build.sh --service swish-scrape

# Copy source code folder
COPY . .

# Remove id_rsa and build.sh
RUN find . -type f -name 'build.sh' -delete

# Add PYTHONPATH
ENV PYTHONPATH /services/swish/swish-scrape/

# User must be appannie
USER swish

CMD ["/bin/bash", "scripts/main.sh"]
