FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir -p /app/data && chmod 777 /app/data

EXPOSE 8000

RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
python manage.py collectstatic --noinput 2>/dev/null || echo "No static files to collect"\n\
python manage.py runserver 0.0.0.0:8000\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]