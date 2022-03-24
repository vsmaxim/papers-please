FROM python:3.9-alpine

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# setup chromedriver
RUN apk update
RUN apk add --no-cache chromium chromium-chromedriver
ENV DISPLAY=:99

# setup the script
WORKDIR app
RUN apk add --no-cache musl-dev libc-dev gcc libffi-dev
COPY . .
RUN pip install .
CMD ["python", "-um", "papers_please"]