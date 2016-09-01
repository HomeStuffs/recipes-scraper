FROM scrapy-base

COPY . /runtime/app
RUN cd /runtime/app
RUN pip install -r requirements.txt
