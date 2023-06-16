from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import json
import time

class Crawler(ABC):
    def __init__(self,driver,producer):
        self.driver=driver
        self.producer=producer
        self.num_news=0

    def load_url(self,url,wait=1):
        self.driver.get(url)
        time.sleep(wait)

    @abstractmethod
    def extract_info(self):
        pass

    @abstractmethod
    def collect_data(self):
        pass


class BaoThanhNienCrawler(Crawler):
    def __init__(self,driver,producer):
        super(BaoThanhNienCrawler,self).__init__(driver,producer)

    def extract_info(self):
        
        data={}
        data['title']=self.driver.find_element(By.CSS_SELECTOR,"h1[class='detail-title']").text
        data['summary']=self.driver.find_element(By.CSS_SELECTOR,"h2[class='detail-sapo']").text
        data['content']=self.driver.find_element(By.CSS_SELECTOR,"div[class='detail-content afcbc-body']").text

        categories=self.driver.find_elements(By.CSS_SELECTOR,"div[class='detail-cate']>*")
        data['main_category']=categories[0].text

        data['author']=self.driver.find_element(By.CSS_SELECTOR,"a[class='name']").text

        try:
            data['sub_categories']=[category.text for category in categories[1:]]
        except:
            pass
        
        try:
            data['email']=self.driver.find_element(By.CSS_SELECTOR,"span[class='email']").text
        except:
            pass
        
        data['tags']=[tag.text for tag in self.driver.find_elements(By.CSS_SELECTOR,"div[class='detail-tab']>*")]

        data['comments']=int(self.driver.find_element(By.CSS_SELECTOR,"p[class='text']>*").text)

        return data

    def collect_data(self,topic):
        
        while True:
            container=self.driver.find_element(By.CSS_SELECTOR,"div[class='box-category-middle list__main_check']")    
            list_news=container.find_elements(By.CSS_SELECTOR,"div[class='box-category-item']")[self.num_news:]
            for news in list_news:
                
                self.num_news+=1
                link=news.find_element(By.CSS_SELECTOR,"a[class='box-category-link-with-avatar img-resize']").get_attribute('href')
                try:
                    data={
                        'news_id':news.get_attribute('data-id'),
                        'link':link,
                        'upload':news.find_element(By.CSS_SELECTOR,"div[class='box-time time-ago']").get_attribute('title')
                    }
                    
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.get(link)
                    
                    data.update(self.extract_info())
                    self.driver.close()
                    
                    value=json.dumps(data)
                    self.producer.produce(topic,value=value)
                    self.producer.flush()
                except:pass

                self.driver.switch_to.window(self.driver.window_handles[0])

            actions=ActionChains(self.driver)

            try:
                load_more=self.driver.find_element(By.CSS_SELECTOR,"a[class='view-more btn-viewmore']")
                actions.click(load_more).perform()
            except:
                target=self.driver.find_element(By.CSS_SELECTOR,"div[class='section__muasam']")
                actions.drag_and_drop(list_news[-1], target).perform()


class BaoTuoiTreCrawler(Crawler):
    def __init__(self,driver,producer):
        super(BaoTuoiTreCrawler,self).__init__(driver,producer)

    def extract_info(self):
        data={}
        data['title']=self.driver.find_element(By.CSS_SELECTOR,"h1[class='detail-title article-title']").text
        data['summary']=self.driver.find_element(By.CSS_SELECTOR,"h2[class='detail-sapo']").text
        data['content']=self.driver.find_element(By.CSS_SELECTOR,"div[class='detail-content afcbc-body']").text
        data['author']=self.driver.find_element(By.CSS_SELECTOR,"a[class='name']").text
        categories=self.driver.find_elements(By.CSS_SELECTOR,"div[class='detail-cate']>*")
        data['main_category']=categories[0].text
        data['tags']=[tag.text for tag in self.driver.find_elements(By.CSS_SELECTOR,"div[class='detail-tab']>*")]
        comments=self.driver.find_element(By.CSS_SELECTOR,"span[class='box-head']").text.replace("Bình luận (","").replace(')','')
        data['comments']=int(comments)

        try:
            data['sub_categories']=[category.text for category in categories[1:]]
        except:
            pass

        return data

    def collect_data(self,topic):
        while True:

            list_news=self.driver.find_elements(By.CSS_SELECTOR,"div[class='box-category-item']")[self.num_news:]
            for news in list_news:
                self.num_news+=1          
                link=news.find_element(By.CSS_SELECTOR,"a[class='box-category-link-with-avatar img-resize']").get_attribute("href")
                try:
                    data={
                        'news_id':news.find_element(By.CSS_SELECTOR,"h3[class='box-title-text']").get_attribute('data-comment'),
                        'link':link,
                        'upload':news.find_element(By.CSS_SELECTOR,"span[class='time-ago-last-news']").get_attribute('title')
                    }
                    
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.get(link)
                    
                    data.update(self.extract_info())
                    self.driver.close()
                    
                    value=json.dumps(data)
                    self.producer.produce(topic,value=value)
                    self.producer.flush()
                except:pass
                
                self.driver.switch_to.window(self.driver.window_handles[0])
            
            actions=ActionChains(self.driver)

            try:
                load_more=self.driver.find_element(By.CSS_SELECTOR,"a[class='view-more']")
                actions.click(load_more).perform()
            except:
                target=self.driver.find_element(By.CSS_SELECTOR,"div[class='section__muasam']")
                actions.drag_and_drop(list_news[-1], target).perform()
    
class VNExpressCrawler(Crawler):
    def __init__(self,driver,producer):
        super(VNExpressCrawler,self).__init__(driver,producer)

    def extract_info(self):
        data={}

        data['title']=self.driver.find_element(By.CSS_SELECTOR,"h1[class='title-detail']").text
        data['summary']=self.driver.find_element(By.CSS_SELECTOR,"p[class='description']").text
        paragraphs=self.driver.find_elements(By.CSS_SELECTOR,"p[class='Normal']")
        data['content']="".join([p.text for p in paragraphs[:-1]])
        data['author']=paragraphs[-1].text
        header=self.driver.find_element(By.CSS_SELECTOR,"div[class='header-content width_common']")
        categories=header.find_elements(By.CSS_SELECTOR,"ul[class='breadcrumb']>li")
        data['main_category']=categories[0].text
        data['sub_categories']=[category.text for category in categories[1:]]
        data['upload']=header.find_element(By.CSS_SELECTOR,"span[class='date']").text
        data['tags']=[tag.text for tag in self.driver.find_elements(By.CSS_SELECTOR,"h4[class='item-tag']")]
        try:
            data['comments']=self.driver.find_element(By.ID,"total_comment").text
        except:
            pass
        
        return data

    def collect_data(self,topic):
        while True:
            container=self.driver.find_element(By.CSS_SELECTOR,"div[class='width_common list-news-subfolder']")
            list_news=container.find_elements(By.XPATH,"//article[contains(@class,'item-news') and contains(@class,'item-news-common')]")[self.num_news:]
            
            for news in list_news:
                try:
                    link=news.find_element(By.CSS_SELECTOR,"h3[class='title-news']>a").get_attribute('href')
                    data={
                        'news_id':link.split("-")[-1][:-5],
                        'link':link
                    }
                    
                    self.num_news+=1
                    
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.get(link)

                    data.update(self.extract_info())   
                    self.driver.close()

                    value=json.dumps(data)
                    self.producer.produce(topic,value=value)
                    self.producer.flush()
                except:pass              

                self.driver.switch_to.window(self.driver.window_handles[0])
                
            actions=ActionChains(self.driver) 
            load_more=self.driver.find_element(By.CSS_SELECTOR,"a[class='btn-page next-page ']")
            actions.click(load_more).perform()   
            

            
def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))