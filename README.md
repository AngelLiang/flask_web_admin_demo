# flask web admin demo

flask web 后台模板

主要基于以下模块：

- flask-user
- flask-admin
- start-bootstrap-admin-2

## 快速开始

Windows PowerShell pip：

```PowerShell
python3 -m venv venv
.\venv\Scripts\activate
python3 -m pip install -U pip
pip3 install -U setuptools
pip3 install -r .\requirements.txt

flask initdb
flask createsuperuser
flask run
```

## Docker

```bash
docker build -t flask_app .
docker run -p 5000:5000 -ti flask_app 
```

## gunicorn启动

```bash
gunicorn wsgi:app -c deploy/gunicorn_config.py
# OR
./gunicorn_bootstrap.sh
```

## 效果图

![login](screenshot/login.png)

![admin](screenshot/admin.png)
