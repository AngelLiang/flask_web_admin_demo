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
.\venv\Scripts\Activate.ps1

# 升级pip和setuptools
(venv) python3 -m pip install --upgrade pip
(venv) pip3 install -U setuptools

# 安装依赖包
(venv) pip3 install -r .\requirements.txt
# 从阿里云镜像下载
(venv) pip3 install -r .\requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# 从豆瓣镜像下载
(venv) pip3 install -r .\requirements.txt -i http://mirrors.douban.com/pypi/simple/ --trusted-host mirrors.douban.com

# 拷贝并编辑配置文件
(venv) cp conf_example.py conf.py
(venv) vim conf.py

(venv) flask initdb
(venv) flask createsuperuser
(venv) flask run
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

## 注意事项

- `.env`文件内不能有非ascii编码的字符，也就是不能有中文字符。

## 效果图

![login](screenshot/login.png)

![admin](screenshot/admin.png)
