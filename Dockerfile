###############################################################################
#
# usage:
# > docker build -t flask_app .
# > docker run -p 5000:5000 -ti flask_app 
# > docker inspect <CONTAINER ID> | grep IPAddress
###############################################################################
# OS
FROM centos:7

###############################################################################
# config

# 设置环境变量
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.utf8

# 时区
RUN ln -s -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 设置工作目录
WORKDIR /opt
RUN yum install -y epel-release
RUN yum install -y wget net-tools curl

###############################################################################
# install python36
RUN yum install -y python36
RUN ln -s /usr/bin/python36 /usr/bin/python3

# install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

# upgrade pip & setuptools
RUN python3 -m pip install -U pip && pip3 install -U setuptools

###############################################################################
# mysql

# RUN wget -i -c http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm
# RUN yum -y install mysql57-community-release-el7-10.noarch.rpm
# RUN yum install -y mysql-community-server
# RUN systemctl start mysqld.service

###############################################################################
# clean
RUN yum clean all
RUN rm -rf /tmp/* /var/tmp/*

###############################################################################
### app
RUN mkdir /var/flask_app
WORKDIR /var/flask_app

# install python requirements
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt \
    -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


# RUN pip3 install pipenv
# COPY Pipfile ./
# COPY Pipfile.lock ./
# RUN pipenv install

###############################################################################
# copy project

COPY . .
# COPY .env ./
# COPY app ./
# COPY wsgi.py ./
# COPY tests ./
# COPY deploy ./

# 环境变量
# ENV FLASK_ENV=prodection

# Port to expose
EXPOSE 5000

# RUN flask initdb
# RUN export LC_ALL=en_US.utf8 && export LANG=en_US.utf8 && flask run -h 0.0.0.0 -p 5000
# RUN flask run -h 0.0.0.0 -p 5000
# ENTRYPOINT ["./gunicorn_bootshrap.sh"]

# CMD flask run -h 0.0.0.0 -p 5000
