import requests
from bs4 import BeautifulSoup


def request_seatnum(seatnumber):
    headers = {'authority': 'shbabbek.com','referer': 'https://shbabbek.com/natega',}
    response = requests.get(f'https://shbabbek.com/natega/{seatnumber}', headers=headers)
    return response


def get_stud_data(soup):
    tables = soup.find_all('tr', class_='dataTable__title')
    personal_info = tables[0].parent.parent.find('tbody').find_all('tr')
    subject_tags = tables[1].parent.parent.select('tbody > tr')

    seat_num = int(personal_info[0].find_all('td')[1].text.strip())
    name = list(personal_info[1].children)[3].text.strip()
    school = personal_info[2].find_all('td')[1].a.text.strip()
    edu_adm = personal_info[3].find_all('td')[1].a.text.strip()
    branch = personal_info[4].find_all('td')[1].text.strip()
    total = float(personal_info[5].find_all('td')[1].strong.text.strip())
    pcntg = float(personal_info[6].find_all('td')[1].strong.text.strip()[:-1])
    status = personal_info[8].find_all('td')[1].text.strip()

    stud_subjects = []
    for i, sub in enumerate(subject_tags):
        mark = sub.find_all('td')[1].text
        # if not re.match(re.compile('[+-]?([0-9]*[.])?[0-9]+'), mark): mark = None
        stud_subjects.append(mark.strip())

    with open('results_first_round.csv', 'a', encoding='utf-8-sig') as f2:
        f2.write(f"{seat_num},{name},{school},{edu_adm},{branch},{total},{pcntg},{status},{stud_subjects[0]},{stud_subjects[1]},{stud_subjects[2]},{stud_subjects[3]},{stud_subjects[4]},{stud_subjects[5]},{stud_subjects[6]},{stud_subjects[7]},{stud_subjects[8]},{stud_subjects[9]},{stud_subjects[10]},{stud_subjects[11]},{stud_subjects[12]},{stud_subjects[14]},{stud_subjects[15]},{stud_subjects[16]}\n")


def check_seatnum(_seatnum):
    response = request_seatnum(_seatnum)
    soup = BeautifulSoup(response.content)
    valid = (soup.find('p',attrs={'style':"font-size: 14px;color: red; margin-top: 11px;"}).text=='')
    if valid: get_stud_data(soup)
    else: return _seatnum

if __name__ == '__main__':
    print("High School Results Scraper from Shbabbek.com")
    print("By: Aly Eyad")
    with open('results_first_round.csv', 'w', encoding='utf-8-sig') as f:
        f.write('seat_number,name,school,educational_administration,branch,total,percentage,status,arabic,first_foreign_lang,second_foreign_lang,pure_math,history,geography,philosophy,psychology,chemistry,biology,geology,applied_math,physics,religion,citizenship_education,economics\n')
    start = int(input("Enter the start of the range: "))
    finish = int(input("Enter the end of the range: ")) + 1
    for num in range(start, finish):
        print(f"Checking {num}...")
        num_status = check_seatnum(num)
        if not num_status: print(f'{num} is valid')
        else: print(f'{num} is invalid')
    input("\nEnter any Character to Exit\n")