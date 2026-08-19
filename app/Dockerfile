FROM python:alpine3.24
WORKDIR /app
LABEL "author"="elessar"
LABEL "version"="1.0.0"
COPY requirements.txt .
RUN pip install -r requirements.txt
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"
RUN addgroup -S gdevops && adduser -S -D -G gdevops devops
COPY --chown=devops:gdevops . .
USER devops:gdevops
CMD ["python", "app.py"]
