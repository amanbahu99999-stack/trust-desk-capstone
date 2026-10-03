FROM python:3.12-slim
WORKDIR /app
COPY app.py ./
COPY static ./static
RUN mkdir -p /app/data
ENV PORT=8000 TRUSTDESK_DB=/app/data/trustdesk.db
EXPOSE 8000
VOLUME ["/app/data"]
CMD ["python", "app.py"]
