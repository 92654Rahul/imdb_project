# Clone Repository
git clone https://github.com/92654Rahul/imdb_project.git

# imdb_project:- root project directory

## Getting Started
### Step1: Building docker file
```
cd /imdb_project/
docker build -f DockerFile .
```
### Step2: Enter app container
```
docker images
docker run -i -t {imageid} /bin/bash
```
### Step3: Run imdb spider
```
cd /imdb_scraper
scrapy crawl imdb_spider
```
### Step 4: output file will be generated inside imdb_scraper folder:
```
Example:- data_2024-09-07_15-17-17.json  
          data_{%Y-%m-%d_HH-MM-SS}.json
```
