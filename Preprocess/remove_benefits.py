
# Can only remove if there is a pattern (using bullet or using double newlines)
def remove_benefits(text, keywords=["phúc lợi", "quyền lợi", "benefit"]):
    # Find first existed keywords and use it as keyword
    keywords_indx = []
    for keyword in keywords:
        position = text.lower().find(keyword.lower())
        keywords_indx.append(position)

    existed_keywords = [indx for indx in keywords_indx if indx >= 0]
    
    # Find the position of the keyword
    position = min(existed_keywords)
    # Find the index of the first and last newline before the keyowrd
    newline_before = text.rfind('\n', 0, position)
    newline_after = text.find('\n', position)

    # Determine the index of the first character after the newline(s) after the keyword
    first_bullet_indx = newline_after
    while first_bullet_indx < len(text) and text[first_bullet_indx] == '\n':
        first_bullet_indx += 1
    first_bullet = text[first_bullet_indx]

    # Find the index of the second character after the newline(s) after the keyword
    second_bullet_indx = text.find('\n', first_bullet_indx) + 1
    second_bullet = text[second_bullet_indx]

    # Check if bullet is used
    bullet_check = False
    if first_bullet == second_bullet:
        bullet_check = True
    else:
        bullet_check = False

    # Find the last character index
    cur_bullet_indx = first_bullet_indx
    if bullet_check == True:
        while True:
            next_bullet_indx = text.find('\n', cur_bullet_indx) + 1
            if next_bullet_indx >= len(text):
                end_indx = len(text)
                break
            if text[next_bullet_indx] != first_bullet:
                end_indx = next_bullet_indx - 1
                break
            cur_bullet_indx = next_bullet_indx
    else:
        end_indx = text.find("\n\n", first_bullet_indx)

    # Delete benefits
    found_substring = text[newline_before:end_indx]
    new_text = text.replace(found_substring, "")
    return new_text


text = """
YÊU CẦU:
o Tốt nghiệp Cao đẳng trở lên
o Tiếng Anh giao tiếp TOEIC 550 trở lên, Vi tính văn phòng
o Có kinh nghiệm làm việc 1-2 năm, kỹ năng giao tiếp, thuyết phục & chăm sóc khách hàng
Kinh Doanh, Phát Triển Thị Trường, Quan Hệ Khách Hàng, Tư Vấn, Chăm Sóc Khách Hàng

PHÚC LỢI:
o Lương 15-20 TR +PC - 14 tháng lương/năm – Đánh giá tăng lương hàng năm
o Thưởng cao theo năng lực hàng Quý, các dịp Lễ, Tết
o Làm việc 5 ngày/tuần Từ T2 đến T6 
o Xe hơi công tác, Laptop cá nhân, phụ cấp công tác, điện thoại
o Nhiều cơ hội học tập & đào tạo tại nước ngoài
o Bảo hiểm, ngày phép theo Luật hiện hành + bonus 2 ngày phép/năm
o Du lịch hàng năm, Teambuilding hàng tháng, quý, năm.
o Môi trường làm việc năng động, chuyên nghiệp, cơ hội thăng tiến phát triển bản thân;
"""

print(remove_benefits(text=text))