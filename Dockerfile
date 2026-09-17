FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Deps first so a source-only change does not reinstall them.
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# `compilescss` only finds the stock {% sass_src %} tag, not our {% sass_src_v %},
# so libsass compiles every non-partial .scss into staticfiles/ directly, then
# collectstatic gathers everything (compressed) for WhiteNoise to serve.
RUN python -c "import sass; sass.compile(dirname=('portal/static', 'staticfiles'), output_style='compressed')" \
    && python manage.py collectstatic --noinput \
    && chmod +x docker-entrypoint.sh

RUN useradd --uid 1000 --no-create-home --home-dir /app app \
    && chown -R app:app /app
USER app

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-"]
