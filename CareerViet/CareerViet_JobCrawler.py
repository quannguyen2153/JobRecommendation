# import libraries
from bs4 import BeautifulSoup
import time
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import csv
import unicodedata 
import re
import json

class CareerViet_JobsCrawler():
    def __init__(self, driver, file_path) -> None:
        self.driver = driver
        self.file_path = file_path
    
    # read a link file
    def readFile(self):
        data = []
        with open(self.file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)
        return data
    
    # crawl first template
    def crawl_default_template(self, url, company_img):
        #setup
        info = []
        self.driver.get(url)
        time.sleep(randint(1, 3))

        html = self.driver.page_source 
        soup = BeautifulSoup(html, "html.parser")

        # add basic data
        job_title = soup.find('h1', class_='title').get_text()
        info.append(job_title)
        info.append(url)

        company = soup.find("a", class_="employer job-company-name")
        company_name = company.get_text()
        info.append(company_name)
        company_link = company.get('href')
        info.append(company_link)
        info.append(company_img)

        # column 1
        col1 = soup.find("div", class_="col-lg-4 col-sm-6 item-blue").find('p').find_all('a')
        location = [i.get_text() for i in col1]

        # column 2
        col2 = soup.find_all("div", class_="col-lg-4 col-sm-6 item-blue")[1].find_all('li')
        date = col2[0].find('p').get_text()
        
        fields = col2[1].find('p').find_all('a')
        fields_ls = [i.get_text().lstrip().rstrip() for i in fields]
        
        # column 3
        col3 = soup.find_all("div", class_="col-lg-4 col-sm-6 item-blue")[2].find_all('li')
        salary, exp, position, due_date = None, None, None, None

        # some attributes maybe don't have values
        for i in range(len(col3)):
            if col3[i].find('strong').get_text() == 'Lương':
                salary = col3[i].find('p').get_text()
            elif col3[i].find('strong').get_text() == 'Kinh nghiệm':
                exp = col3[i].find('p').get_text()
            elif col3[i].find('strong').get_text() == 'Cấp bậc':
                position = col3[i].find('p').get_text()
            elif col3[i].find('strong').get_text() == 'Hết hạn nộp':
                due_date = col3[i].find('p').get_text()

        info.append(location)
        info.append(date)
        info.append(due_date)
        info.append(fields_ls)
        info.append(salary)
        info.append(" ".join(exp.split())) if exp is not None else info.append(None)
        info.append(position)

        # push all benefits to a list
        try:
            benefits = [i.get_text() for i in soup.find("ul", class_="welfare-list").find_all("li")]
            info.append(benefits)
        except:
            info.append(None)

        # normalize text
        description = re.sub(r'\n+', '\n', soup.find("div", class_="detail-row reset-bullet").get_text(separator="\n"))
        info.append(unicodedata.normalize("NFKD", description))

        requirements = re.sub(r'\n+', '\n', soup.find_all("div", class_="detail-row")[2].get_text(separator="\n"))
        info.append(unicodedata.normalize("NFKD", requirements))

        return info

    # crawl second template
    def crawl_new_template(self, url, company_img):
        # setup
        info = []
        self.driver.get(url)
        time.sleep(randint(1, 3))

        html = self.driver.page_source 
        soup = BeautifulSoup(html, "html.parser")

        # add basic data
        job_title = soup.find(class_='title').get_text().strip()
        info.append(job_title)
        info.append(url)
        
        company = soup.find("a", class_="company")
        company_name = company.get_text()
        info.append(company_name)
        company_link = company.get('href')
        info.append(company_link)
        info.append(company_img)

        work_place = soup.find("p", class_="list-workplace").find_all('a')
        location = [i.get_text() for i in work_place]

        # this template has only one colummn, all are the same as default template
        col = soup.find('tbody').find_all('tr')
        fields = col[0].find_all('a')
        fields_ls = [i.get_text().lstrip().rstrip() for i in fields]
        salary = col[1].find('td',class_='content').get_text()
        position = col[4].find('td',class_='content').get_text()
        exp = col[5].find('td',class_='content').get_text()
        exp = " ".join(exp.split())
        due_date = col[6].find('td',class_='content').get_text()
        date = col[7].find('td',class_='content').get_text()

        info.append(location)
        info.append(date)
        info.append(due_date)
        info.append(fields_ls)
        info.append(salary)
        info.append(exp)
        info.append(position)

        try:
            benefits = [i.get_text() for i in soup.find("ul", class_="welfare-list").find_all("li")]
            info.append(benefits)
        except:
            info.append(None)

        full_content = soup.find("div", class_="full-content")
        description = re.sub(r'\n+', '\n', full_content.find("div", class_="detail-row").get_text(separator="\n"))
        info.append(unicodedata.normalize("NFKD", description))

        requirements = re.sub(r'\n+', '\n', full_content.find_all("div", class_="detail-row")[1].get_text(separator="\n"))
        info.append(unicodedata.normalize("NFKD", requirements))

        return info
    
    # crawl first template, if cannot, continue crawling second template, if then cannot, continue (some templates are unique)
    def crawl(self):
        # get link file then crawl all links
        links = self.readFile()
        results = []
        for i in range(len(links)):
            try:
                info = self.crawl_default_template(links[i][0], links[i][1])
                results.append(info)
            except:
                try:
                     info = self.crawl_new_template(links[i][0], links[i][1])
                     results.append(info)
                except:
                    continue
        return results
    
    # write data to json file
    def writeFile(self, data, output_file):
        tags = ["job_title", "job_url", "company_name", "company_url", "company_img_url", "location", "post_date", "due_date", "fields", "salary", "experience", "position", "benefits", "job_description", "requirements"]
        json_data = [{k: v for k, v in zip(tags, sublist)} for sublist in data]

        with open(output_file, "w", encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    option= webdriver.ChromeOptions()
    option.add_argument("--incognito")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
        
    CV_LinkCrawler = CareerViet_JobsCrawler(driver=driver, file_path="D:\\Grab\\Bootcamp\\CareerViet_links.csv")
    results = CV_LinkCrawler.crawl()
    CV_LinkCrawler.writeFile(results, "D:\\Grab\\Bootcamp\\data\\CareerViet_jobs.json")

    driver.close()