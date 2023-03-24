FROM python:3.10-alpine3.13
LABEL maintainer="fastapidemo"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirement.txt /tmp/requirement.txt
COPY ./script/run.sh /run.sh

COPY ./app /app
WORKDIR /app
EXPOSE 8001


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirement.txt && \
    rm -rf /tmp && \
    chmod +x /run.sh

ENV PATH="/py/bin:$PATH"

CMD ["sh", "/run.sh"]