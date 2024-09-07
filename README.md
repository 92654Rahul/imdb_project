# imdb_project
root project directory

## Getting Started
### Step1: Building and running docker file
```
cd /imdb_project/
docker build -f DockerFile .
```
### Step2: Enter app container and  scrapy crawler
```
docker images
docker run -i -t {imageid} /bin/sh

### Step3: go inside folder and exucute below commands
cd /imdb_scraper
scrapy crawl imdb_spider
```

