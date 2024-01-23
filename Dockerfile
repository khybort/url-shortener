# Build stage
FROM python:3.9 as builder
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python -m venv /venv
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9
WORKDIR /app
COPY --from=builder /app /app
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"
COPY . .
EXPOSE 8086
CMD ["python", "manage.py", "runserver", "0.0.0.0:$SERVER_PORT"]