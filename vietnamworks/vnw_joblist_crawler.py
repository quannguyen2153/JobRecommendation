from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random
import time

import os
import json

import traceback



class VNWJobListCrawler():
    def __init__(self, sorting, service, driver) -> None:
        self.sorting = sorting
        self.org_url = "https://www.vietnamworks.com/viec-lam?sorting={}".format(self.sorting)
        
        self.service = service
        self.driver = driver
    
    def extractJobInformation(self, job_element):
        job_info = {
            'title': '',
            'job_url': '',
            'company': '',
            'company_url': '',
            'salary': '',
            'location': ''
        }
        
        icon = job_element.find_element(By.XPATH, ".//*") \
                        .find_element(By.XPATH, ".//*") \
                        .find_element(By.XPATH, ".//*")
            
        info = icon.find_element(By.XPATH, "following-sibling::*")

        title_element = info.find_element(By.XPATH, ".//*")
        title = title_element.find_element(By.XPATH, ".//a[@href]")

        job_info['job_url'] = title.get_attribute("href")
        job_info['title'] = title.text
            
        company_element = title_element.find_element(By.XPATH, "following-sibling::*").find_element(By.XPATH, "following-sibling::*")
        try:
            company = company_element.find_element(By.XPATH, ".//a[@href]")
            job_info['company_url'] = company.get_attribute("href")
        except:
            company = company_element.find_element(By.XPATH, ".//span")

        job_info['company'] = company.text
            
        salary_location_element = company_element.find_element(By.XPATH, "following-sibling::*")
        salary_location = salary_location_element.find_elements(By.XPATH, ".//span")

        job_info['salary'] = salary_location[0].text
        job_info['location'] = salary_location[1].text
        
        return job_info
    
    def crawlJobList(self, output_dir, page=1, timeout=5):
        job_info_list = []
        
        while True:    
            try:
                if page <= 1:
                    page = 1
                    self.driver.get(self.org_url)
                else:
                    self.driver.get("https://www.vietnamworks.com/viec-lam?page={}&sorting={}".format(page, self.sorting))
                
                for i in range(50):
                    job_selector = ".search_list.view_job_item.item-{}.new-job-card".format(i)

                    # Wait for the presence of the element with the specified CSS selector
                    try:
                        job = WebDriverWait(self.driver, timeout).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, job_selector))
                        )
                    except:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        job = WebDriverWait(self.driver, timeout).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, job_selector))
                        )

                    job_info_list.append(self.extractJobInformation(job))
                    
                    print('Complete crawling job {} at page {}'.format(i + 1, page))
                    
                print('--------------- Complete crawling jobs at page {} ---------------'.format(page))

                if page % 50 == 0:
                    json_file = 'vnw_joblist_{}.json'.format(page)
                    output_path = os.path.join(output_dir, json_file)
                    
                    with open(output_path, "w", encoding="utf-8") as file:
                        json.dump(job_info_list, file, indent=4, ensure_ascii=False)
                    print('Wrote 50 job pages to {}.'.format(json_file))
                    
                    job_info_list = []
                
                breaking_time = random.randint(int(timeout/2), timeout)
                print('Breaking time: {}...'.format(breaking_time))
                time.sleep(breaking_time)
                
                page += 1
            
            except:
                traceback.print_exc()
                
                json_file = 'vnw_joblist_{}.json'.format(page)
                output_path = os.path.join(output_dir, json_file)
                
                with open(output_path, "w", encoding="utf-8") as file:
                    json.dump(job_info_list, file, indent=4, ensure_ascii=False)
                print('An error occured. Saved crawled job pages to {}.'.format(json_file))
                
                break
            
if __name__ == '__main__':
    service = Service(executable_path="vietnamworks/drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    vnw_joblist_crawler = VNWJobListCrawler(sorting='lasted', service=service, driver=driver)
    vnw_joblist_crawler.crawlJobList(output_dir='vietnamworks/rawdata', page=1, timeout=5)
    
    driver.quit()