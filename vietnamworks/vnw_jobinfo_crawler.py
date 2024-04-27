from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# import random
import time

import os
import json
import pandas as pd

import traceback

class VNWJobInfoCrawler():
    def __init__(self, driver) -> None:
        self.driver = driver
        
    def extractFullJobInformation(self, url):
        self.driver.get(url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        job_info_dict = {
            'title': '',
            'salary': '',
            'end_date': '',
            'job_description': '',
            'requirements': '',
            'benefits': [],
            'post_date': '',
            'profession': '',
            'field': '',
            'pos_rank': '',
            'skills': '',
            'profile_language': '',
            'experienced_year': '',
            'nationality': '',
            'location': '',
            'tags': [],
            'company': '',
            'contact': [url]
        }
        
        try:
            full_view_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Xem đầy đủ mô tả công việc']"))
            )
            full_view_button.click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            try:        
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                full_view_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Xem đầy đủ mô tả công việc']"))
                )
                full_view_button.click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except TimeoutException:
                pass
            except:
                traceback.print_exc()

        rows = self.driver.find_elements(By.ID, "vnwLayout__row")

        title = rows[4].find_element(By.XPATH, ".//h1")
        title = title.text
        job_info_dict['title'] = title

        salary = rows[5].find_element(By.XPATH, ".//span")
        salary = salary.text
        job_info_dict['salary'] = salary

        end_date = rows[6].find_element(By.XPATH, ".//span")
        end_date = end_date.text
        job_info_dict['end_date'] = end_date

        job_info = rows[8].find_elements(By.XPATH, "//h2")

        job_description = job_info[0].find_element(By.XPATH, "following-sibling::*")
        job_description = job_description.text
        job_info_dict['job_description'] = job_description

        requirements = job_info[1].find_element(By.XPATH, "following-sibling::*")
        requirements = requirements.text
        job_info_dict['requirements'] = requirements

        benefits = rows[9].find_elements(By.ID, "vnwLayout__col")
        for benefit in benefits:
            job_info_dict['benefits'].append(benefit.text)
            
        job_extra_info = rows[11].find_elements(By.ID, "vnwLayout__col")

        col0 = job_extra_info[0].find_element(By.NAME, "paragraph")
        post_date = col0.text
        col1 = job_extra_info[1].find_element(By.NAME, "paragraph")
        pos_rank = col1.text
        col2 = job_extra_info[2].find_element(By.NAME, "paragraph")
        profession = col2.text
        col3 = job_extra_info[3].find_element(By.NAME, "paragraph")
        skills = col3.text
        col4 = job_extra_info[4].find_element(By.NAME, "paragraph")
        field = col4.text
        col5 = job_extra_info[5].find_element(By.NAME, "paragraph")
        profile_language = col5.text
        col6 = job_extra_info[6].find_element(By.NAME, "paragraph")
        experienced_year = col6.text
        col7 = job_extra_info[7].find_element(By.NAME, "paragraph")
        nationality = col7.text

        job_info_dict['post_date'] = post_date
        job_info_dict['profession'] = profession
        job_info_dict['field'] = field
        job_info_dict['pos_rank'] = pos_rank
        job_info_dict['skills'] = skills
        job_info_dict['profile_language'] = profile_language
        job_info_dict['experienced_year'] = experienced_year
        job_info_dict['nationality'] = nationality

        location = rows[13].find_element(By.NAME, "paragraph")
        location = location.text
        job_info_dict['location'] = location

        tags = rows[14].find_elements(By.ID, "vnwLayout__col")[1].find_elements(By.XPATH, ".//span")
        for tag in tags:
            job_info_dict['tags'].append(tag.text)
            
        company = rows[2].find_element(By.ID, "vnwLayout__col") \
                        .find_element(By.XPATH, "following-sibling::*") \
                        .find_element(By.NAME, "label")
        company = company.text
        job_info_dict['company'] = company
        
        return job_info_dict
    
    def crawlJobInformation(self, joblist_path, output_dir, job_idx=1):
        df = pd.read_json(joblist_path, encoding="utf-8")
        
        jobs = []

        for url in df['job_url'][job_idx-1:]:
            # breaking_time = random.randint(1, 3)
            
            try:
                job = self.extractFullJobInformation(url)
                jobs.append(job)
                print('Crawled job {}: {} from {}.'.format(job_idx, job['title'], job['company']))
            except:
                print('Job {} has been removed.'.format(job_idx))
                print('Job {}\'s url: {}.'.format(job_idx, url))
                traceback.print_exc()
            
            if job_idx % 500 == 0:
                json_file = 'vnw_jobinfo_{}.json'.format(job_idx)
                output_path = os.path.join(output_dir, json_file)
                
                with open(output_path, "w", encoding="utf-8") as file:
                    json.dump(jobs, file, indent=4, ensure_ascii=False)
                print('Wrote 1000 jobs to {}.'.format(json_file))
                jobs = []
            
            job_idx += 1
            
            # print('Breaking time: {}...'.format(breaking_time))
            # time.sleep(breaking_time)
        
if __name__ == "__main__":
    service = Service(executable_path="vietnamworks/drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    vnw_jobinfo_crawler = VNWJobInfoCrawler(driver=driver)
    vnw_jobinfo_crawler.crawlJobInformation(joblist_path='vietnamworks/rawdata/joblist/vnw_joblist_full.json',
                                            output_dir='vietnamworks/rawdata/jobinfo/segments',
                                            job_idx=3001)
    
    driver.quit()