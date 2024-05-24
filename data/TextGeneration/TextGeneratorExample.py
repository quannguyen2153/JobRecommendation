import PyPDF2
from TextGenerator import TextGenerator
from CVParser import CVParser
from JobChatBot import JobChatBot

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
TOKEN = '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'

text_generator = TextGenerator(api_url=API_URL, token=TOKEN)    
cv_parser = CVParser(text_generation_api_url=API_URL, token=TOKEN, cv_format_path='TextGeneration/cv_form.txt')

pdf_path = 'TextGeneration/sample_cv2.pdf'
cv_dict = cv_parser.parseFromPDF(cv_pdf_path=pdf_path)

cv_dict = cv_parser.standardizeCVDict(cv_dict)


jobchatbot = JobChatBot(text_generation_api_url=API_URL, token=TOKEN)    
job_dict = {
        "job_title":"MT Sales Supervisor - Khu Vực Hà Nội",
        "job_url":"https:\/\/www.vietnamworks.com\/mt-sales-supervisor-khu-vuc-ha-noi-1763221-jv?source=searchResults&searchType=2&placement=1770721&sortBy=latest",
        "company_name":"Otsuka Thang Nutrition Co.,ltd.",
        "company_url":"https:\/\/www.vietnamworks.com\/nha-tuyen-dung\/otsuka-thang-nutrition-co-ltd--c132178",
        "location":"Ha Noi",
        "post_date":1712509200.0,
        "due_date":1715619600.0,
        "fields":"Bán Lẻ\/Tiêu Dùng > Quản Lý Khu Vực",
        "salary":"$680 - $970",
        "experience":None,
        "position":"Nhân viên",
        "benefits":[
            "Thưởng\nThưởng tháng 13, tháng 14 theo hiệu quả công việc",
            "Chăm sóc sức khoẻ\nBảo hiểm sức khỏe BIC toàn diện",
            "Máy tính xách tay\nMáy tính xách tay"
        ],
        "job_description":"I. KEY RESPOSIBILITIES:\n\n1. Area Management (40%):\n• Understand the operation of customers in the area of responsibility.\n• Manage KPI targets for each client in the responsible area.\n• Control inventory - sell out of customers in the area of responsibility.\n• Plan and control promotion programs, activities and cost (coverage, hiring, promotion plan, sales support activities, POSM…). \n• Establish trusting relationships with clients for mutual benefits.\n2. Staff Management (30%):\n• Create effective sales pathways (sales, regions, opportunities, etc.).\n• Deploy and oversee the Sale Representative team's KPI implementation.\n• Make sure the team adheres to company requirements in its market execution.\n• Training Plan - Building Team\n• Build and maintain relationships with related departments.\n3. Data Management (20%):\n• In responsible of managing data related to sales, stores, allocation ratios, etc.\n• Present the activity plan via weekly\/monthly\/other frequency.\n• Deliver reports as requested.\n4. Localized Solutions (10%):\n• Find solutions and specific steps for regional development.\n• Idea or proposal to expand the responsible area.",
        "requirements":"REQUIREMENT\n• Min: Bachelor’s Degree, Ideal: Financial, Sales & Marketing Knowledge\n• Has at least 2 years of experience in the position of Sale Supervisor MT.\n• Experience with the beverage industry is an advantage.\n• Leadership & interpersonal skills.\n• Good command of computer and statistics.\n• Strong analytical and planning skills, Customer business analysis.\n• Focused on outcomes, analytical in the details.\n• Decision-making based on facts and principles, as well as value-based management abilities.\n• Good communication skills in both Vietnamese and English.\n• Priority management, proactive, good analytic and critical thinking.\n• Have ability to build relationship with customer\n\nBENEFIT:\n• Working hours: from Mon to Fri (8:00– 17:00). \n• Annual leaves: 15 days per year. \n• Sick leaves: 4 days per year. \n• Covid leaves: no limited. \n• Performance Appraisal: one per year. \n• Bonus of 13th and bonus of Performance Evaluation based on company policy. \n• Others: annual health checkup, general medical insurance (BIC insurance)"
    }
jobchatbot.attachJob(job_dict=job_dict)
print(jobchatbot.job_requirements)

jobchatbot.attachCV(cv_dict)
print(jobchatbot.cv_text)

response = jobchatbot.query(message="Which are requirements that the candidate does not meet for this job?")
print(response)