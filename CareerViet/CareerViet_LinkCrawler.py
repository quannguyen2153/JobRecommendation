from bs4 import BeautifulSoup
import time
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class CareerViet_LinkCrawler():
    def __init__(self, driver) -> None:
        self.driver = driver
    def crawl_JobLinks(self, output_file):
        links = []
        i = 1
        url = "https://careerviet.vn/viec-lam/tat-ca-viec-lam-sortdv-trang-{}-vi.html"
        while True:
            self.driver.get(url.format(i)) 
            time.sleep(randint(3, 5)) 

            html = self.driver.page_source 
            soup = BeautifulSoup(html, "html.parser") 

            anchor_element = soup.find_all('div', class_='caption')
            for element in anchor_element:
                links.append(element.find('a', class_='job_link').get('href'))

            flag = soup.find('li', class_='next-page')
            if not flag:
                break
            i = i + 1

        unique_links = list(set(links))
        with open(output_file, 'w+') as f:
            for link in unique_links:
                f.write('%s\n' %link)
        f.close()

if __name__ == '__main__':
    option= webdriver.ChromeOptions()
    option.add_argument("--incognito")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
        
    CV_LinkCrawler = CareerViet_LinkCrawler(driver=driver)
    CV_LinkCrawler.crawl_JobLinks(output_file='D:\\Grab\\Bootcamp\\CareerViet_links.txt')
        
    driver.close()