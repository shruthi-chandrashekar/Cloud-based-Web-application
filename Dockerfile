FROM alpine:3.7

WORKDIR /app

COPY . /app

RUN apk add --no-cache python && \
    python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip install --trusted-host pypi.python.org -r req.txt

EXPOSE 80

ENV TEAM_ID=CC_425_377_404_413

CMD ["python","8000.py"]
