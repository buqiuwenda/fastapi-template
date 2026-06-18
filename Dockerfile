FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 先装依赖，利用 Docker 层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再拷贝应用代码
COPY app ./app

ENV APP_HOST=0.0.0.0 \
    APP_PORT=8000

EXPOSE 8000

# 与 Makefile 一致：模块路径 app.main:app，host/port 可通过环境变量覆盖
CMD uvicorn app.main:app --host $APP_HOST --port $APP_PORT
