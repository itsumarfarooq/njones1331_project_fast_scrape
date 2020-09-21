import scrapy
import re

class EventectiveScraperSpider(scrapy.Spider):
    name = 'eventective_scraper'
    allowed_domains = ['eventective.com']
    with open('urls_to_scrape.txt') as f:
        start_urls = [url.strip() for url in f.readlines()]

    def parse(self, response):
        event = {}
        event[response.url]=event_info = {}
        event_info['Title'] = response.xpath('//h1/text()').get()
        event_info['Address'] = response.xpath(
            '//div[@class="h4 eve-address-nav eve-hover-pointer"]/text()').get()
        event_info['Phone'] = response.xpath('//div[@class="provider-phone"]/text()').get()
        event_info['Visible Website'] = response.xpath('//a[contains(@onclick,"PrUrlClick")]/text()').get().strip() if response.xpath('//a[contains(@onclick,"PrUrlClick")]/text()').get() else response.xpath('//a[contains(@onclick,"PrUrlClick")]/text()').get()
        event_info['Linked Website URL'] = response.xpath('//a[contains(@onclick,"PrUrlClick")]/@href').get()
        event_info['Capacity'] = response.xpath('//li[contains(text(),"Capacity:")]/text()').get()
        event_info['About'] = response.xpath(
            '///div[@id="providerInfo"]/div/text()').get()
        for span_elem in response.xpath('//span[./b]'):
            key_text = span_elem.xpath('./b/text()').get()
            event_info[key_text] = [text.strip() for text in span_elem.xpath(
                './following-sibling::*/li/text()').getall() if text]
        event_info['Packages'] = {}
        n = 1
        for package_div in response.xpath('//h2[text()="Package Pricing"]/following-sibling::div/div[contains(@id,"eve-package")]'):
            package_info = {}
            package_info['Title'] = package_div.xpath(
                './div[@class="eve-rect-body"]/div[@class="h4 eve-ellipsis"]/text()').get()
            package_info['Description'] = package_div.xpath(
                'normalize-space(./div[@class="eve-rect-body"]/div[@class="h4 eve-ellipsis"]/following-sibling::span[@class="hidden-xs"])').get()
            package_info['Pricing'] = package_div.xpath(
                'normalize-space(./div[@class="eve-rect-footer hidden-xs text-center" and ./div[@class="eve-price-highlight h4"]])').get()
            if package_info['Title']:
                event_info['Packages'][n] = package_info
                n += 1
        event_info['Spaces Available'] = response.xpath(
            '//div[contains(@id,"eve-space")]/div[@class="eve-box-header eve-event-space"]/div[@class="text-center eve-ellipsis"]/text()').getall()
        event_info['Image URLs'] = response.xpath('//div[@class="carousel-cell"]/img/@data-flickity-lazyload').getall()
        yield event
