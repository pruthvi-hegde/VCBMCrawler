import scrapy
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from urllib.parse import urlparse
from scrapy.selector import Selector
import json


# `scrapy crawl abstract` from inside VCBMCrawler
class EgworkSpider(CrawlSpider):
    name = 'abstract'
    allowed_domains = ['diglib.eg.org']
    start_urls = [
        'https://diglib.eg.org/handle/10.2312/466/recent-submissions',
        'https://diglib.eg.org/handle/10.2312/466/recent-submissions?offset=20',
        'https://diglib.eg.org/handle/10.2312/465',
        'https://diglib.eg.org/handle/10.2312/464',
        'https://diglib.eg.org/handle/10.2312/7762/recent-submissions',
        'https://diglib.eg.org/handle/10.2312/7762/recent-submissions?offset=20',
        'https://diglib.eg.org/handle/10.2312/13225/recent-submissions',
        'https://diglib.eg.org/handle/10.2312/13225/recent-submissions?offset=20',
        'https://diglib.eg.org/handle/10.2312/2630861/recent-submissions',
        'https://diglib.eg.org/handle/10.2312/2630861/recent-submissions?offset=20',
        'https://diglib.eg.org/handle/10.2312/2631687/recent-submissions',
        'https://diglib.eg.org/handle/10.2312/2631687/recent-submissions?offset=20',
        'https://diglib.eg.org/handle/10.2312/2632660/recent-submissions',
        'https://diglib.eg.org/handle/10.2312/2632660/recent-submissions?offset=20',
        'https://diglib.eg.org/handle/10.2312/2632802/recent-submissions',
        'https://diglib.eg.org/handle/10.2312/2632802/recent-submissions?offset=20',
        'https://diglib.eg.org/handle/10.2312/2632935',
        'https://diglib.eg.org/handle/10.2312/2633086'
        ]
    base_url = 'https://diglib.eg.org'

    rules = (
        Rule(LinkExtractor(allow=[r'handle/10.2312/vcbm', 'handle/10.2312/VCBM.']), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # selector of pdf file.
        o = urlparse(response.url)
        structured_link = o.scheme + "://" + o.netloc + o.path

        hxs = Selector(response)
        publication_title = hxs.xpath('//title/text()').get()
        abstract = hxs.xpath('//meta[@name="DCTERMS.abstract"]/@content').get()
        citation_keywords = hxs.xpath('//meta[@name="DC.subject"]/@content').get()
        article_authors = hxs.xpath('//meta[@name="DC.creator"]/@content').getall()
        dirname = os.getcwd()
        #collection_path = os.path.join(dirname, "publicationsDownload/abstracts/")
        collection_path = os.path.join(dirname, "VCBMCrawler/articles_titles_and_abstract/")
        #collection_path = os.path.join(dirname, "publicationsDownload/articles_metadata/")

        # file_name = publication_title.replace('/', '-') + ".json"

        file_name = publication_title.replace('/', '-') + ".txt"
        save_path = os.path.join(collection_path, file_name)
        #
        # data = {
        #     'keywords': citation_keywords,
        #     'article_authors': article_authors
        #
        # }
        # json_string = json.dumps(data)
        # print(json_string)

        try:
            self.logger.info('Saving PDF %s', save_path)
            with open(save_path, 'w') as file:
                file.write(file_name.replace(".txt", ". "))
                file.write(abstract)
        except FileExistsError:
            print("File Exist")


    # def save_pdf(self, response):
    #     """ Save pdf files """
    #     file_name = (response.meta.get('publication_title')).replace('/', '-') + ".pdf"
    #     dirname = os.getcwd()
    #     collection_path = os.path.join(dirname, "publications/")
    #
    #     save_path = os.path.join(collection_path, file_name)
    #
    #     self.logger.info('Saving PDF %s', save_path)
    #     with open(save_path, 'wb') as file:
    #         file.write(response.body)
