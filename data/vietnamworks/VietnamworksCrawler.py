from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import random
import time

import os
import json
import csv

import pandas as pd

import traceback



class VNWCrawler():
    def __init__(self, driver, sorting) -> None:        
        self.driver = driver
        self.sorting = sorting
    
    def extractJobCardInformation(self, job_element, timeout=5):
        job_info = {
            'job_title': '',
            'job_url': '',
            'company_name': '',
            'company_url': '',
            'company_img_url': '',
            'salary': '',
            'location': []
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
        job_info['job_title'] = title.text
            
        # Locate and extract the company name and url
        company_element = title_element.find_element(By.XPATH, "following-sibling::*").find_element(By.XPATH, "following-sibling::*")
        try:
            company = company_element.find_element(By.XPATH, ".//a[@href]")
            job_info['company_url'] = company.get_attribute("href")
        except:
            company = company_element.find_element(By.XPATH, ".//span")

        job_info['company_name'] = company.text
            
        # Locate and extract the salary and location
        salary_location_element = company_element.find_element(By.XPATH, "following-sibling::*")
        salary_location = salary_location_element.find_elements(By.XPATH, ".//span")

        job_info['salary'] = salary_location[0].text
        job_info['location'].append(salary_location[1].text)
        
        return job_info
    
    def crawlJobList(self, output_path, page=1, timeout=5):
        fieldnames = ('job_title', 'job_url', 'company_name', 'company_url', 'company_img_url', 'salary', 'location')
        
        if page == 1:
            with open(output_path, 'a') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
        
        # Crawl until reached the end of vietnamworks job list
        while True:    
            try:
                # Open the job list page
                if page <= 1:
                    page = 1
                    url = "https://www.vietnamworks.com/viec-lam?sorting={}".format(self.sorting)
                    self.driver.get(self.org_url)
                else:
                    url = "https://www.vietnamworks.com/viec-lam?page={}&sorting={}".format(page, self.sorting)                              
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

                    job_info = self.extractJobCardInformation(job, timeout)

                    # Write the job to csv
                    with open(output_path, 'a', encoding='utf-8') as file:
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writerow(job_info)
                    
                    print('Complete crawling job {} at page {}'.format(i + 1, page))
                    
                print('--------------- Complete crawling jobs at page {} ---------------'.format(page))
                    
                # Breaking time to avoid ban
                breaking_time = random.randint(int(timeout/2), timeout)
                print('Breaking time: {}...'.format(breaking_time))
                time.sleep(breaking_time)
                
                page += 1
            
            except:
                traceback.print_exc()                
                break
            
    def extractFullJobInformation(self, job_url, company_url, company_img_url):
        # Open the job website
        self.driver.get(job_url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        job_info_dict = {
            'job_title': '',
            'job_url': job_url,
            'company_name': '',
            'company_url': company_url,
            'company_img_url': company_img_url,
            'location': [],
            'post_date': '',
            'due_date': '',
            'fields': [],
            'salary': '',
            'experience': '',
            'position': '',
            'benefits': [],
            'job_description': '',
            'requirements': '',
            'area': '',
            'skills': '',
            'profile_language': '',
            'nationality': '',
            'tags': [],
            'job_site': 'Vietnamworks'
        }
        
        # Click button to view full job details
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

        # Extract the job title
        title = rows[4].find_element(By.XPATH, ".//h1")
        title = title.text
        job_info_dict['job_title'] = title

        # Extract the salary
        salary = rows[5].find_element(By.XPATH, ".//span")
        salary = salary.text
        job_info_dict['salary'] = salary

        # Extract the due date
        end_date = rows[6].find_element(By.XPATH, ".//span")
        end_date = end_date.text
        job_info_dict['due_date'] = end_date

        # Extract the job description and requirements
        job_info = rows[8].find_elements(By.XPATH, "//h2")

        job_description = job_info[0].find_element(By.XPATH, "following-sibling::*")
        job_description = job_description.text
        job_info_dict['job_description'] = job_description

        requirements = job_info[1].find_element(By.XPATH, "following-sibling::*")
        requirements = requirements.text
        job_info_dict['requirements'] = requirements

        # Extract the benefits
        benefits = rows[9].find_elements(By.ID, "vnwLayout__col")
        for benefit in benefits:
            job_info_dict['benefits'].append(benefit.text)
            
        # Extract the job extra info
        job_extra_info = rows[11].find_elements(By.ID, "vnwLayout__col")

        col0 = job_extra_info[0].find_element(By.NAME, "paragraph")
        post_date = col0.text
        col1 = job_extra_info[1].find_element(By.NAME, "paragraph")
        position = col1.text
        col2 = job_extra_info[2].find_element(By.NAME, "paragraph")
        field = col2.text
        col3 = job_extra_info[3].find_element(By.NAME, "paragraph")
        skills = col3.text
        col4 = job_extra_info[4].find_element(By.NAME, "paragraph")
        area = col4.text
        col5 = job_extra_info[5].find_element(By.NAME, "paragraph")
        profile_language = col5.text
        col6 = job_extra_info[6].find_element(By.NAME, "paragraph")
        experienced_year = col6.text
        col7 = job_extra_info[7].find_element(By.NAME, "paragraph")
        nationality = col7.text

        job_info_dict['post_date'] = post_date
        job_info_dict['fields'].append(field)
        job_info_dict['area'] = area
        job_info_dict['position'] = position
        job_info_dict['skills'] = skills
        job_info_dict['profile_language'] = profile_language
        job_info_dict['experience'] = experienced_year
        job_info_dict['nationality'] = nationality

        # Extract the location
        location = rows[13].find_element(By.NAME, "paragraph")
        location = location.text
        job_info_dict['location'].append(location)

        # Extract the tags
        tags = rows[14].find_elements(By.ID, "vnwLayout__col")[1].find_elements(By.XPATH, ".//span")
        for tag in tags:
            job_info_dict['tags'].append(tag.text)
            
        # Extract the company name
        company = rows[2].find_element(By.ID, "vnwLayout__col") \
                        .find_element(By.XPATH, "following-sibling::*") \
                        .find_element(By.NAME, "label")
        company_name = company.text
        job_info_dict['company_name'] = company_name
        
        return job_info_dict
    
    def crawlJobInformation(self, joblist_df, output_path, job_idx=1):        
        fieldnames = ('job_title', \
                      'job_url', \
                      'company_name', \
                      'company_url', \
                      'company_img_url', \
                      'location', \
                      'post_date', \
                      'due_date', \
                      'fields', \
                      'salary', \
                      'experience', \
                      'position', \
                      'benefits', \
                      'job_description', \
                      'requirements', \
                      'area', \
                      'skills', \
                      'profile_language', \
                      'nationality', \
                      'tags', \
                      'job_site')
        
        if job_idx == 1:
            with open(output_path, 'a') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

        for index, row in joblist_df.iloc[job_idx:].iterrows():
            job_url = row['job_url']
            company_url = row['company_url']
            company_img_url = row['company_img_url']
            
            try:
                job = self.extractFullJobInformation(job_url, company_url, company_img_url)
                
                # Write the job to csv
                with open(output_path, 'a', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writerow(job)
                
                print('Crawled job {}: {} from {}.'.format(job_idx, job['job_title'], job['company_name']))
            except:
                print('Job {} has been removed.'.format(job_idx))
                print('Job {}\'s url: {}.'.format(job_idx, job_url))
                traceback.print_exc()
            
            job_idx += 1
            
if __name__ == '__main__':
    service = Service(executable_path="vietnamworks/drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    vnw_joblist_crawler = VNWCrawler(driver=driver, sorting='lasted')
    
    # vnw_joblist_crawler.crawlJobList(output_path='vietnamworks/rawdata/joblist.csv', page=1, timeout=5)
    
    joblist_df = pd.read_csv('vietnamworks/rawdata/joblist.csv')
    vnw_joblist_crawler.crawlJobInformation(joblist_df=joblist_df, output_path='vietnamworks/rawdata/jobinfo.csv', job_idx=1)
    
    driver.quit()