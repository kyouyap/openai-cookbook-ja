FROM python:3.9.6

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get -y update && apt-get upgrade -qqy && apt-get -y install \
        bash \
        curl \
        gcc \
        git \
        jq \
        ffmpeg
# Apply https://github.com/pypa/setuptools/pull/3108
RUN pip install --upgrade setuptools

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH