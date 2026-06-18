VENV :=/Users/joannayang/wenda/my_agent_314/venv
PYTHON := $(VENV)/bin/python3.14
PIP := $(VENV)/bin/pip3.14
UVICORN := $(VENV)/bin/uvicorn


# install
install:
	$(PIP) install -r requirements.txt


# 启动项目（需在项目根目录执行，以便 import app）
start:
	set -a; [ -f .env ] && . ./.env; set +a; \
	$(UVICORN) app.main:app --reload --host $${APP_HOST:-0.0.0.0} --port $${APP_PORT:-8000}


# 退出venv
exit:
	deactivate
