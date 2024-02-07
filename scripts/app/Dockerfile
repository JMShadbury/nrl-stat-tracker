
FROM python:3.9-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY util/requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 80
CMD ["python", "view_stats.py"]
