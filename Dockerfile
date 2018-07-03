#
# docker build -t flask_demo .
# docker run -p 5000:5000 -ti flask_demo 
# docker inspect <CONTAINER ID> | grep IPAddress

FROM centos:7

# 设置环境变量
ENV LANG en_US.UTF-8

# 时区
RUN ln -s -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

WORKDIR /opt

# install python36
RUN yum install -y epel-release
RUN yum install -y python36
RUN ln -s /usr/bin/python36 /usr/bin/python3

# install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

# 升级pip
RUN pip3 install -U pip
# 升级setuptools
RUN pip3 install -U setuptools

# test
# CMD ["pip3", "-V"]

# 清理
RUN yum clean all
RUN rm -rf /tmp/* /var/tmp/*

###############################################################################
# install requirements
RUN mkdir /app
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# RUN pip3 install pipenv
# COPY Pipfile ./
# COPY Pipfile.lock ./
# RUN pipenv install
# RUN pipenv shell

COPY . .
# COPY app ./
# COPY wsgi.py ./

# 环境变量
ENV FLASK_ENV=prodection

# Port to expose
EXPOSE 5000

# RUN flask initdb
# RUN export LC_ALL=en_US.utf8 && export LANG=en_US.utf8 && flask run -h 0.0.0.0 -p 5000
# RUN flask run -h 0.0.0.0 -p 5000
# ENTRYPOINT ["./gunicorn_bootshrap.sh"]

CMD flask run -h 0.0.0.0 -p 5000
