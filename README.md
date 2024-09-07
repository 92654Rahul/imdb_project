# scrapy-docker
basic scrapy project running on docker container and connect to docker container of mongo

## Getting Started
### Step1: Building and running docker container by docker-compose
```
cd /path/to/project
docker-compose up -d
```
### Step2: Enter scrapyapp container and running scrapy crawler
```
docker ps
docker exec -it {scrapyapp_container_id} /bin/sh
cd /home/src/ExampleCrawler
scrapy crawl example
```

### Create new crawler in docker container
```
cd /home/src
scrapy genspider example example.com
```
