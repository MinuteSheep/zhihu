# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.items import ZhihuItem


class UserSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['www.zhihu.com']
    start_user = 'zhang-jia-wei'
    user_url = 'https://www.zhihu.com/api/v4/members/%s?include=%s'
    user_include = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    followings_url = 'https://www.zhihu.com/api/v4/members/%s/followees?include=%s&offset=20&limit=20'
    followings_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_url = 'https://www.zhihu.com/api/v4/members/%s/followers?include=%s&offset=20&limit=20'
    followers_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield scrapy.Request(self.user_url % (self.start_user, self.user_include), callback=self.parse_user)

    def parse_user(self, request):
        item = ZhihuItem()
        results = json.loads(request.text)
        for field in item.fields:
            if field in results.keys():
                item[field] = results.get(field)
        yield item
        yield scrapy.Request(self.followings_url % (results.get('url_token'), self.followings_include),
                             callback=self.parse_followings)
        yield scrapy.Request(self.followers_url % (results.get('url_token'), self.followers_include),
                             callback=self.parse_followers)

    def parse_followings(self, request):
        results = json.loads(request.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url % (result.get('url_token'), self.user_include),
                                     callback=self.parse_user)
        if 'paging' in results.keys() and results.get('paging').get('is_end') == 'false':
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page, callback=self.parse_followings)

    def parse_followers(self, request):
        results = json.loads(request.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url % (result.get('url_token'), self.user_include),
                                     callback=self.parse_user)
        if 'paging' in results.keys() and results.get('paging').get('is_end') == 'false':
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page, callback=self.parse_followers)
