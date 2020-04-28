import time
import os

while True:
    os.system("scrapy crawl udn")
    time.sleep(30)#每三十秒自動爬取一次