import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.gov.uk/search/news-and-communications?keywords=environment&order=relevance&page=1']

    def parse(self, response):
        # Extract URLs of the articles
        article_links = response.css('a.gem-c-document-list__item-title::attr(href)').getall()
        print(f'Found {len(article_links)} articles on page {response.url}')
    
        for link in article_links:
            yield response.follow(link, self.parse_article)
    
        # Follow the link to the next page
        next_page_link = response.css('div.govuk-pagination__next a.govuk-link::attr(href)').get()
        if next_page_link:
            yield response.follow(next_page_link, self.parse)


    def parse_article(self, response):
        # Extract the title and content of the article
        title = response.css('h1::text').get()
        content = response.css('.govuk-body').get()

        # Yield a dictionary containing the title, content, and URL of the article
        yield {
            'title': title,
            'content': content,
            'url': response.url
        }
