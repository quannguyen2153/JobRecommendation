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
    def __init__(self, profession, sorting, driver) -> None:
        self.profession = profession
        self.sorting = sorting
        
        if profession is None:
            self.org_url = "https://www.vietnamworks.com/viec-lam?sorting={}".format(self.sorting)
        else:
            self.org_url = "https://www.vietnamworks.com/viec-lam?g={}&sorting={}".format(self.profession, self.sorting)
        
        self.driver = driver
    
    def extractJobInformation(self, job_element, timeout=5):
        job_info = {
            'title': '',
            'job_url': '',
            'company': '',
            'company_url': '',
            'company_img_url': '',
            'salary': '',
            'location': ''
        }
        
        # Locate and extract the company image url 
        icon = job_element.find_element(By.XPATH, ".//*") \
                        .find_element(By.XPATH, ".//*") \
                        .find_element(By.XPATH, ".//*")
                        
        class RealImage(object):
            def __init__(self, locator, substring):
                self.locator = locator
                self.substring = substring

            def __call__(self, driver):
                element = driver.find_element(*self.locator)
                src = element.get_attribute("src")
                if self.substring in src:
                    return element
                else:
                    return False
        
        img_element = icon.find_element(By.XPATH, ".//img")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", img_element)    
        img_element = WebDriverWait(icon, timeout).until(
            RealImage((By.XPATH, ".//img"), "http")
        )  
        img_url = img_element.get_attribute("src")
        job_info['company_img_url'] = img_url
            
        # Locate and extract the job title and url
        info = icon.find_element(By.XPATH, "following-sibling::*")

        title_element = info.find_element(By.XPATH, ".//*")
        title = title_element.find_element(By.XPATH, ".//a[@href]")

        job_info['job_url'] = title.get_attribute("href")
        job_info['title'] = title.text
            
        # Locate and extract the company name and url
        company_element = title_element.find_element(By.XPATH, "following-sibling::*").find_element(By.XPATH, "following-sibling::*")
        try:
            company = company_element.find_element(By.XPATH, ".//a[@href]")
            job_info['company_url'] = company.get_attribute("href")
        except:
            company = company_element.find_element(By.XPATH, ".//span")

        job_info['company'] = company.text
            
        # Locate and extract the salary and location
        salary_location_element = company_element.find_element(By.XPATH, "following-sibling::*")
        salary_location = salary_location_element.find_elements(By.XPATH, ".//span")

        job_info['salary'] = salary_location[0].text
        job_info['location'] = salary_location[1].text
        
        return job_info
    
    def crawlJobList(self, output_dir, page=1, save_steps=50, timeout=5):
        job_info_list = []
        
        # Crawl until reached the end of vietnamworks job list
        while True:    
            try:
                # Open the job list page
                if page <= 1:
                    page = 1
                    self.driver.get(self.org_url)
                else:
                    if self.profession is None:
                        url = "https://www.vietnamworks.com/viec-lam?page={}&sorting={}".format(page, self.sorting)
                    else:
                        url = "https://www.vietnamworks.com/viec-lam?g={}&page={}&sorting={}" \
                              .format(self.profession, page, self.sorting)
                              
                    self.driver.get(url)
                    
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Loop through each job card (there are 50 cards per page)
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

                    job_info_list.append(self.extractJobInformation(job, timeout))
                    
                    print('Complete crawling job {} at page {}'.format(i + 1, page))
                    
                print('--------------- Complete crawling jobs at page {} ---------------'.format(page))

                # Write the job list to json after every save_steps
                if page % save_steps == 0:
                    json_file = 'vnw_joblist_{}.json'.format(page)
                    output_path = os.path.join(output_dir, json_file)
                    
                    with open(output_path, "w", encoding="utf-8") as file:
                        json.dump(job_info_list, file, indent=4, ensure_ascii=False)
                    print('Wrote {} job pages to {}.'.format(save_steps, json_file))
                    
                    job_info_list = []
                
                breaking_time = random.randint(int(timeout/2), timeout)
                print('Breaking time: {}...'.format(breaking_time))
                time.sleep(breaking_time)
                
                page += 1
            
            except:
                traceback.print_exc()
                
                # Write the job list if encounter errors
                json_file = 'vnw_joblist_{}.json'.format(page)
                output_path = os.path.join(output_dir, json_file)
                
                with open(output_path, "w", encoding="utf-8") as file:
                    json.dump(job_info_list, file, indent=4, ensure_ascii=False)
                print('An error occured. Saved crawled job pages to {}.'.format(json_file))
                
                break
            
if __name__ == '__main__':
    service = Service(executable_path="vietnamworks/drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    vnw_joblist_crawler = VNWJobListCrawler(profession=None, sorting='lasted', driver=driver)
    vnw_joblist_crawler.crawlJobList(output_dir='vietnamworks/rawdata/joblist/segments2', page=1, timeout=5)
    
    driver.quit()