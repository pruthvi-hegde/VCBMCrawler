import scrapy
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from urllib.parse import urlparse
from scrapy.selector import Selector
import json


# use this command to run this file.
# `scrapy crawl meta` from inside VCBMCrawler

class EgworkSpider(CrawlSpider):
    name = 'meta'
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

        article_authors = hxs.xpath('//meta[@name="DC.creator"]/@content').getall()
        article_contributors = hxs.xpath('//meta[@name="DC.contributor"]/@content').getall()

        publisher = hxs.xpath('//meta[@name="DC.publisher"]/@content').get()
        published_year =  hxs.xpath('//meta[@name="DCTERMS.issued"]/@content').get()

        article_details = hxs.xpath('//meta[@name="DC.identifier"]/@content').getall()
        citation_keywords = hxs.xpath('//meta[@name="DC.subject"]/@content').getall()
        dirname = os.getcwd()
        collection_path = os.path.join(dirname, "VCBMCrawler/article_metadata")

        file_name = publication_title.replace('/', '-') + ".json"

        #file_name = publication_title.replace('/', '-') + ".txt"
        save_path = os.path.join(collection_path, file_name)

        data = {
             'article_title' : publication_title,
             'article_authors': ','.join(str(e).replace(","," ") for e in article_authors if article_authors is not None),
             #'article_contributors' : article_contributors,
             'publisher' : publisher,

             'published_year' : published_year,
             'ISSN': article_details[0],
             'ISBN': article_details[1],
              'DOI' : article_details[2],

             'keywords': ','.join(str(e).replace(","," ") for e in citation_keywords if citation_keywords is not None),
             'abstract': abstract
        }
        json_string = json.dumps(data)
        # print(json_string)

        try:
            self.logger.info('Saving json file %s', save_path)
            if data['abstract'] is not None:
                with open(save_path, 'w') as file:
                    file.write(json_string)
            else:
                print("Not a valid publication")
        except FileExistsError:
            print("File Exist")



