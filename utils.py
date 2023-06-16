from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from src.crawler import BaoThanhNienCrawler,BaoTuoiTreCrawler,VNExpressCrawler
from confluent_kafka import Producer
import json

NEWS_URL={
    "bao_thanh_nien":"https://thanhnien.vn/tin-moi.htm",
    "bao_tuoi_tre":"https://tuoitre.vn/tin-moi-nhat.htm",
    "vnexpress":"https://vnexpress.net/tin-tuc-24h"
}

NEWS_CLASS={
    "bao_thanh_nien":BaoThanhNienCrawler,
    "bao_tuoi_tre":BaoTuoiTreCrawler,
    "vnexpress":VNExpressCrawler
}

def prepare(args):
    options=Options()
    options.add_experimental_option('detach',True)
    options.add_argument('headless')
    options.add_argument('start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver=Chrome(chrome_options=options,executable_path='chromedriver')

    producer = Producer({'bootstrap.servers': 'localhost:9092'})

    try:
        crawler=NEWS_CLASS[args.news](driver,producer)
        crawler.load_url(NEWS_URL[args.news],3)
    except:
        raise Exception(f'Not supported currently.')

    return crawler

def crawling_data(args):
    crawler=prepare(args)
    crawler.collect_data(args.topic)

