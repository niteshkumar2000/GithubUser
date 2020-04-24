# -*- coding: utf-8 -*-
import scrapy


class GituserSpider(scrapy.Spider):
    name = 'GitUser'

    def __init__(self, username=None, *args, **kwargs):
        super(GituserSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.github.com/%s' % username]

    def parse(self, response):
        # pinned_repo = {}
        # for i in range(1, 6):
        #     repo = {
        #         'name': '',
        #         'desc': '',
        #         'lang': ''
        #     }
        #     try:
        #         repo['name'] = (response.xpath('..//div[@class="js-pinned-items-reorder-container"]//ol//li[' +str(i)  + ']//text()').extract()[6]).strip()
        #     except IndexError:
        #         break
        #     repo['desc'] = (response.xpath('..//div[@class="js-pinned-items-reorder-container"]//ol//li[' +str(i)  + ']//text()').extract()[10]).strip()
        #     repo['lang'] = (response.xpath('..//div[@class="js-pinned-items-reorder-container"]//ol//li[' +str(i)  + ']//text()').extract()[15]).strip()
        #     pinned_repo.update({str(i): repo})
        data = {
            'UserName' : response.xpath('..//h1//span[@itemprop="additionalName"]//text()').extract_first(),
            'DisplayName' : response.xpath('..//h1//span[@itemprop="name"]//text()').extract_first(),
            'Image' : response.xpath('..//a[@itemprop="image"]//@href').extract_first(),
            'Location' : response.xpath('..//li[@itemprop="homeLocation"]//span//text()').extract_first(),
            'Website' : response.xpath('..//li[@itemprop="url"]//a//text()').extract_first(),
            'Contribution' : (response.xpath('..//h2[@class="f4 text-normal mb-2"]//text()').extract_first()).strip().replace("\n       ",''),
            'Repocount' : (response.xpath('..//span[@class="Counter hide-lg hide-md hide-sm"]//text()').extract()[0]).strip(),
            'Project' : (response.xpath('..//span[@class="Counter hide-lg hide-md hide-sm"]//text()').extract()[1]).strip(),
            'Stars' : (response.xpath('..//span[@class="Counter hide-lg hide-md hide-sm"]//text()').extract()[2]).strip(),
            'Followers' : (response.xpath('..//span[@class="Counter hide-lg hide-md hide-sm"]//text()').extract()[3]).strip(),
            'Following' : (response.xpath('..//span[@class="Counter hide-lg hide-md hide-sm"]//text()').extract()[4]).strip(),
            'Bio': response.xpath('..//div[@class="js-profile-editable-area"]//div//div//text()').extract_first()
        }
        yield data


