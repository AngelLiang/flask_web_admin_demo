# flask web admin demo

flask web 后台模板

主要基于以下模块：

- flask-user
- flask-admin
- start-bootstrap-admin-2

## 快速开始

Windows PowerShell pipenv+pip：

```PowerShell
# option
$env:PIPENV_VENV_IN_PROJECT = "."
pipenv install

pipenv shell
# or
.\.venv\Scripts\activate

flask initdb
flask createsuperuser
flask run
```

## 效果图

![login](screenshot/login.png)

![admin](screenshot/admin.png)
