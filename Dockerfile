FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl nginx supervisor && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN mkdir -p /data /app/staticfiles /var/log/supervisor

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN rm -f /etc/nginx/sites-enabled/default

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && exec supervisord -n -c /etc/supervisor/conf.d/supervisord.conf"]
