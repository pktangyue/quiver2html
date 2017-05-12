FROM python:3.6-alpine
COPY . /code
WORKDIR /code
RUN pip install -r requirement.txt --index-url http://pypi.douban.com/simple --trusted-host pypi.douban.com
CMD python3
