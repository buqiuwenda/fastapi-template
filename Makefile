VENV :=your_path/my_agent_314/venv
PYTHON := $(VENV)/bin/python3.14
PIP := $(VENV)/bin/pip3.14
UVICORN := $(VENV)/bin/uvicorn


# install
install:
	$(PIP) install -r requirements.txt


# 启动项目（需在项目根目录执行，以便 import app）
start:
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000


# 退出venv
exit:
	deactivate
