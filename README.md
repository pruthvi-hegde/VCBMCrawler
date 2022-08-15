# VCBMCrawler
This repository contains the code to scrape VCBM publications metadata from Eurographics site.

## First Step
Activate your virtual environment and run,
`pip install scrapy`

## To download VCBM publications (2008 - 2021)
Navigate to VCBMCrawler and run,
`scrapy crawl abstract` 

## To scrape metadata of publications,
Navigate to VCBMCrawler and run,
`scrapy crawl meta`

## To merge metadata from publications to single file run,
python merge_all_article_metadata.py 


