import PyPDF2
from TextGenerator import TextGenerator
from CVParser import CVParser
from JobChatBot import JobChatBot

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
TOKEN = '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'

text_generator = TextGenerator(api_url=API_URL, token=TOKEN)    
cv_parser = CVParser(text_generation_api_url=API_URL, token=TOKEN, cv_format_path='TextGeneration/cv_form.txt')

pdf_path = 'TextGeneration/sample_cv.pdf'
cv_info = cv_parser.parseFromPDF(cv_pdf_path=pdf_path)

# print(cv_info)

cv_dict = cv_parser.convertToDict(cv_info)


jobchatbot = JobChatBot(text_generation_api_url=API_URL, token=TOKEN)    
job_dict = {
        "job_title":"Mechanical Service Engineer",
        "job_url":"https:\/\/www.vietnamworks.com\/mechanical-service-engineer--1768459-jv?source=searchResults&searchType=2&placement=1771659&sortBy=latest",
        "company_name":"Công Ty TNHH BHS Corrugated Machinery Việt Nam",
        "company_url":"https:\/\/www.vietnamworks.com\/nha-tuyen-dung\/cong-ty-tnhh-bhs-corrugated-machinery-viet-nam-c154855",
        "location":"Ho Chi Minh, Ho Chi Minh City, Vietnam",
        "post_date":1713718800.0,
        "due_date":1716829200.0,
        "fields":"Khoa Học & Kỹ Thuật > Cơ Khí & Điện Lạnh",
        "salary":"Thương lượng",
        "experience":None,
        "position":"Nhân viên",
        "benefits":[
            "Thưởng\nMức lương hấp dẫn + Thưởng hàng năm",
            "Cơ hội du lịch\nThời gian làm việc linh hoạt",
            "Hoạt động nhóm\nĐược đào tạo và làm việc ở nước ngoài + Cơ hội phát triển và thăng tiến cao"
        ],
        "job_description":"Duties and responsibilities\n1. Mechanical installation and commissioning of corrugated machines include steam piping assembling & supervising.\n2. Troubleshooting and maintenance corrugated machines at customer site.\n3. Start-up the machines, training customer regarding operation, maintenance, and spare parts knowledge.\n4. Advising \/ recommendation on spare parts, maintenance, and other service products to customer.\n5. Installation, commissioning, and service for corrugators and rolls\n6. Support BHS internal staff on service daily business, such as spare parts issue, machine problem advice, upgrade and so on.\n7. Prepare reports according to department regulations.\n8. Maintain relationship with customer.\n9. Other duty and tasks work assigned by supervisor",
        "requirements":"1. Mechanical engineering background, bachelor, or diploma degree.\n2. 2-3 years field experience of maintenance\/troubleshooting to heavy duty machines.\n3. Be ready to travel frequently.\n4. Read and understand mechanical drawings and plant layouts, basic skills in pneumatic \/ hydraulic System-Operations.\n5. Be able to work under pressure, committed, dedicated and conscientious.\n6. Good communication skills.\n7. Good English spoken and written.\n8. Open mind and teamwork."
    }
jobchatbot.attachJob(job_dict=job_dict)
print(jobchatbot.job_requirements)

jobchatbot.attachCV(cv_dict)
print(jobchatbot.cv_text)

response = jobchatbot.query(message="Is this candidate well-suited for this job?")
print(response)