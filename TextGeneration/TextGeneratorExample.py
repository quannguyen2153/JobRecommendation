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

print(cv_info)

cv_dict = cv_parser.convertToDict(cv_info)

    
job_info = "- University graduate majoring in mechanical engineering, mechatronics or other related majors.\n- No experience required\n- Agile and hardworking.\n- Can use Auto CAD and layout making experience.\n- Speaking, listening, writing English intermediate level is required\n\n\n* Benefit\n- Top 100 Vietnam Best Place to work, Top 15 Happy Workforce in Vietnam (Large enterprises), Top 7 in Electronics\/Hi-tech\/Utilities\n- Attractive salary, 13rd month salary, personal KPI annually\n- Working Time: Monday ~ Friday, early out every Friday, Saturday & Sunday off\n- Overtime Claim: 150% Weekdays, 200% Weekends\n- Laptop provided ($1,500)\n- Free Shuttle Bus from Hai Phong, Hai Duong, Thai Binh, Ha Noi (weekend)\n- Free Meal (breakfast, lunch, dinner – if OT)\n- Free Dormitory provided\n- Protection Programs: regular health check, 24\/7 Insurance\n- Team building, opportunities to join Company training courses (including Oversea training, Language training…)\n- Core Member Bonus; Excellent employee awards monthly, quarterly"

jobchatbot = JobChatBot(text_generation_api_url=API_URL, token=TOKEN)
jobchatbot.attachCV(cv_dict)
print(jobchatbot.cv_text)
# jobchatbot.attachJob(job_info)
# response = jobchatbot.query(message="Are there any skills this candidate should improve for this job?")
# print(response)