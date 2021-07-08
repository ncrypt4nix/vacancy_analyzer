import os


BOT_NAME = 'hh'

SPIDER_MODULES = ['hh.spiders']
NEWSPIDER_MODULE = 'hh.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 0.5

# Disable cookies (enabled by default)
COOKIES_ENABLED = False


# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # User Agent
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    # Proxy
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

ITEM_PIPELINES = {
    'hh.pipelines.HhPipeline': 100,
}

# Proxy settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
PROXY_LIST = os.path.join(BASE_DIR, 'proxy_list.txt')
# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
PROXY_MODE = 0
# Retry many times since proxies often fail
RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

LOG_FILE = os.path.join(PROJECT_DIR, 'logs', 'scrapy.log')
LOG_LEVEL = 'INFO'

# Redis conf
REDIS_PREFIX = 'hh'
REDIS_HOST = os.getenv('REDIS_HOST', 'redis-scrapy')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

MAIN_HH_DOMAIN = 'hh.ru'
