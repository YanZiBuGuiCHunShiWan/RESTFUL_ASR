# 声明基础镜像版本，选择pytorch官方镜像
FROM pytorch/pytorch:1.3-cuda10.1-cudnn7-runtime
#FROM   espnet/espnet:gpu-latest
MAINTAINER tianchi <1366402587@qq.com>

COPY ./requirements.txt /requirements.txt

RUN apt-get update -yqq
RUN apt-get install  libsndfile1  uwsgi-plugin-python3 -y


# 将所有代码添加进去
COPY . /data/app

# 设置默认的工作目录
WORKDIR /data/app

# 设置系统编码为utf-8，防止中文乱码
ENV LANG C.UTF-8

# 设置暴露8000端口
EXPOSE 8000

#apt-get install libsndfile1
# CMD启动http服务，（也可以选择启动rpc服务，或者两个同时启动）
#CMD cd /data/app/scripts && sh start_http_server.sh
