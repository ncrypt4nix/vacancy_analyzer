import scrapy
import logging

from hh.settings import MAIN_HH_DOMAIN
from hh.items import HHItem


logger = logging.getLogger()


class HHSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = [MAIN_HH_DOMAIN]
    _start_url = (
        f'https://{MAIN_HH_DOMAIN}/search/vacancy'
        '?text={search}'
        '&fromSearchLine=false'
        '&st=searchVacancy'
    )

    def __init__(self, search=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not search:
            logger.error('You forgot to specify a parsing keyword')
        self._start_url = self._start_url.format(search=search)
        logger.info(f'Parse for search text: {search}')
        self.start_urls = [self._start_url]

    def parse(self, response):
        try:
            page_count = max(map(int, response.css('[data-qa="pager-page"] span::text').getall()))
        except ValueError:
            logger.error('WE WERE DISCOVERED =(')
            return

        for page in range(page_count):
            yield scrapy.Request(self._start_url + f'&page={page}', self.parse_pagination)

    def parse_pagination(self, response):
        for vacancy in response.css('.resume-search-item__name a').xpath('@href').getall():
            yield scrapy.Request(vacancy, self.parse_concrete_page)

    def parse_concrete_page(self, response) -> HHItem:
        """parsing a specific vacancy"""
        vacancy = HHItem()
        vacancy['name'] = response.css('.vacancy-title h1::text').get()
        vacancy['wage'] = response.css('.vacancy-title span::text').get()
        vacancy['skills'] = response.css('.bloko-tag__section_text::text').getall()
        vacancy['url'] = response.url
        vacancy['experience'] = response.css('[data-qa="vacancy-experience"]::text').get()
        vacancy['employment_mode'] = response.css('[data-qa="vacancy-view-employment-mode"]::text').get()
        vacancy['description'] = response.css('[data-qa="vacancy-description"]').get()
        yield vacancy
