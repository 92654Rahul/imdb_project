import json
import scrapy
from scrapy.cmdline import execute
from datetime import datetime

class IMDBSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["imdb.com"]
    domain = "https://www.imdb.com"
    scraped_data = []  # List to store scraped data
    count = 0  # Counter to keep track of how many records have been inserted

    def start_requests(self):
        """
        Initial method that sends the first request to start the spider.
        """
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,gu;q=0.7',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'referer': 'https://www.google.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

        # Starting URL that contains the list of movies or shows
        start_url = "https://www.imdb.com/list/ls055386972/"
        # Sending the request to the start_url and using parse_list_page as callback
        yield scrapy.FormRequest(url=start_url, callback=self.parse_list_page, dont_filter=True, headers=headers)

    def parse_list_page(self, response):
        """
        Method to parse the main listing page and extract URLs for individual items.
        """
        # Extract the JSON-LD data that contains the list of movies or shows
        data = response.xpath('//script[@type="application/ld+json"]/text()').get()

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,gu;q=0.7',
            'priority': 'u=0, i',
            'referer': 'https://www.imdb.com/list/ls055386972/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

        # Load the JSON data to extract individual movie/show URLs
        json_urls = json.loads(data)
        for final in json_urls['itemListElement']:
            final_url = final['item']['url']  # Extract the URL of the item
            # Send a request to the individual item page and use parse_detail_page as callback
            yield scrapy.FormRequest(url=final_url, callback=self.parse_detail_page, dont_filter=True, headers=headers)

    def parse_detail_page(self, response):
        """
        Method to parse individual movie/show pages and extract relevant data.
        """
        # Extract JSON-LD structured data from the page
        data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        json_data = json.loads(data)

        # Extract relevant information like actors, directors, creators
        actor_data = json_data.get('actor', [])
        director_data = json_data.get('director', [])
        creator_data = json_data.get('creator', [])

        # Prepare item dictionary with all extracted data
        item = {
            'title': json_data.get('name'),  # Movie/show title
            'url': json_data['review']['itemReviewed'].get('url'),  # URL of the reviewed item
            'date_created': json_data['review'].get('dateCreated'),  # Date when review was created
            'year_released': json_data.get('datePublished'),  # Year the movie/show was released
            'genre': json_data.get('genre'),  # Genre of the movie/show
            'actors': [person["name"] for person in actor_data],  # List of actors
            'directors': [person["name"] for person in director_data],  # List of directors
            # List of creators, using get() method to avoid missing "name" keys
            'creators': [person.get("name", "N/A") for person in creator_data if person["@type"] == "Person"]
        }

        # Append the item to the scraped_data list
        self.scraped_data.append(item)
        # Increment the counter and print a message
        self.count += 1
        print("Data Inserted", self.count)

    def close(self, reason):
        """
        Method called when the spider finishes, to save the scraped data to a JSON file.
        """
        # Get the current date in 'YYYY-MM-DD' format to use in the filename
        current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"data_{current_date}.json"  # Filename format with current date

        # Save the scraped data to a JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # Run the Scrapy spider from command line
    execute(['scrapy', 'crawl', 'imdb_spider'])
