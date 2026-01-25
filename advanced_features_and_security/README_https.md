HTTPS & Secure Redirects
Django settings (LibraryProject/settings.py)

SECURE_SSL_REDIRECT = not DEBUG → Redirect HTTP→HTTPS in production
HSTS (enabled when DEBUG=False):
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
Secure cookies (enabled when DEBUG=False):
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
Headers:
X_FRAME_OPTIONS = DENY
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
Reverse proxy support (e.g., Nginx/Apache):
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
Environment-driven config:
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = ["127.0.0.1", "localhost"] (set your domain in production)
Optional: CSRF_TRUSTED_ORIGINS = ["https://yourdomain.com", "https://www.yourdomain.com"]
Content Security Policy (CSP)

Added via LibraryProject/middleware.py which sets the Content-Security-Policy header to reduce XSS risk.
Nginx example (TLS + redirect)

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Enforce HTTPS in browsers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Static/media (adjust paths)
    location /static/ { alias /path/to/static/; }
    location /media/  { alias /path/to/media/; }

    # Proxy to Django (gunicorn/uvicorn) on localhost
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

Certbot (Ubuntu quick start)

sudo apt-get update && sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
sudo systemctl reload nginx
Local deploy checks (simulate production)

export DJANGO_DEBUG=False
python manage.py check --deploy
export DJANGO_DEBUG=True
Security review

HTTPS enforced with SECURE_SSL_REDIRECT and HSTS in production.
Cookies restricted to HTTPS (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE).
Clickjacking and MIME sniffing mitigated (X_FRAME_OPTIONS, SECURE_CONTENT_TYPE_NOSNIFF).
CSP enabled to reduce XSS attack surface.
Use SECURE_PROXY_SSL_HEADER behind a reverse proxy and set ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS to your domain(s).