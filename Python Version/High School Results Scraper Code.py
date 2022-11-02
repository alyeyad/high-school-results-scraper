import os
from bs4 import BeautifulSoup
import concurrent.futures

PAGES_PATH = os.getcwd() + '/student_pages/'


def get_stud_data(filename):
    f = open(PAGES_PATH+filename, 'r', encoding='utf-8-sig')
    soup = BeautifulSoup(f)
    f.close()
    print('Extracting '+filename)
    tables = soup.find_all('tr', class_='dataTable__title')
    personal_info = tables[0].parent.parent.find('tbody').find_all('tr')
    subject_tags = tables[1].parent.parent.select('tbody > tr')

    seat_num = int(personal_info[0].find_all('td')[1].text.strip())
    name = list(personal_info[1].children)[3].text.strip()
    school = personal_info[2].find_all('td')[1].a.text.strip()
    edu_adm = personal_info[3].find_all('td')[1].a.text.strip()
    branch = personal_info[4].find_all('td')[1].text.strip()
    total = personal_info[5].find_all('td')[1].strong.text.strip()
    percentage = personal_info[6].find_all('td')[1].strong.text.strip()[:-1]
    status = personal_info[8].find_all('td')[1].text.strip()

    stud_subjects = []
    for i, sub in enumerate(subject_tags):
        mark = sub.find_all('td')[1].text

        stud_subjects.append(mark.strip())

    with open('results_first_round.csv', 'a', encoding='utf-8-sig') as f3:
        f3.write(f"{seat_num},{name},{school},{edu_adm},{branch},{total},{percentage},{status},{stud_subjects[0]},{stud_subjects[1]},{stud_subjects[2]},{stud_subjects[3]},{stud_subjects[4]},{stud_subjects[5]},{stud_subjects[6]},{stud_subjects[7]},{stud_subjects[8]},{stud_subjects[9]},{stud_subjects[10]},{stud_subjects[11]},{stud_subjects[12]},{stud_subjects[14]},{stud_subjects[15]},{stud_subjects[16]}\n")


if __name__ == '__main__':
    print("High School Results Scraper from Shbabbek.com")
    print("By: Aly Eyad")

    with open('results_first_round.csv', 'w', encoding='utf-8-sig') as f2:
        f2.write('seat_number,name,school,educational_administration,branch,total,percentage,status,arabic,'
                 'first_foreign_lang,second_foreign_lang,pure_math,history,geography,philosophy,psychology,chemistry,'
                 'biology,geology,applied_math,physics,religion,citizenship_education,economics\n')

    if not os.path.exists(PAGES_PATH):
        print('Pages Path not found, please run the Downloader Program and try again.')
    else:
        nums_list = os.listdir(PAGES_PATH)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(get_stud_data, nums_list)
