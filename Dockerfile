#
# docker build -t flask_demo .
# docker inspect <CONTAINER ID> | grep IPAddress

FROM centos:7

RUN yum -y groupinstall "Development tools"
RUN yum -y install gcc gcc-c++ gdb wget
RUN yum -y install zlib zlib-devel bzip2-devel openssl-devel openssl-static ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel

###############################################################################
### download python 3.5.4
RUN cd /opt
RUN wget https://www.python.org/ftp/python/3.5.4/Python-3.5.4.tgz
RUN tar xf Python-3.5.4.tgz
# build 
RUN cd Python-3.5.4  \
    && ./configure --prefix=/usr/local --enable-shared  \
    && make \
    && make install
RUN ln -s /usr/local/bin/python3.5 /usr/bin/python3
# link
RUN echo /usr/local/lib >> /etc/ld.so.conf.d/local.conf && ldconfig

# test
# CMD ["python3", "-V"]

###############################################################################
### install setuptools

# 准备工作
RUN yum install -y zlib-devel zip unzip
RUN cd /opt
# download
RUN wget https://pypi.python.org/packages/0f/22/7fdcc777ba60e2a8b1ea17f679c2652ffe80bd5a2f35d61c629cb9545d5e/setuptools-36.7.2.zip#md5=1874983171af0f7b16b5ec48558e6e55
RUN unzip setuptools-36.7.2.zip
# install
RUN cd setuptools-36.7.2    \
    && python3 setup.py build   \
    && python3 setup.py install

###############################################################################
# install pip3
RUN cd /opt
# download
RUN wget https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz#md5=35f01da33009719497f01a4ba69d63c9
RUN tar vxf pip-9.0.1.tar.gz
# install
RUN cd pip-9.0.1 \
    && python3 setup.py install
# link
RUN ln -s /usr/local/bin/pip3 /usr/bin/pip3

# 升级pip
RUN pip3 install -U pip
# 升级setuptools
RUN pip3 install -U setuptools

# test
# CMD ["pip3", "-V"]

###############################################################################
# install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# RUN pip3 install pipenv
# COPY Pipfile ./
# COPY Pipfile.lock ./
# RUN pipenv install
# RUN pipenv shell

COPY . .

# 环境变量
ENV FLASK_ENV=prodection

# Port to expose
EXPOSE 5000

# RUN flask initdb
RUN export LC_ALL=en_US.utf8 && export LANG=en_US.utf8 && flask run -h 0.0.0.0 -p 5000
# RUN flask run -h 0.0.0.0 -p 5000
# ENTRYPOINT ["./gunicorn_bootshrap.sh"]


