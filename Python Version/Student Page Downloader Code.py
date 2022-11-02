import requests
from bs4 import BeautifulSoup
import concurrent.futures
import os

PAGES_PATH = os.getcwd() + '/student_pages/'


def check_seat_num(seat_num):
    if os.path.exists(PAGES_PATH+f'{seat_num}.html'):
        print('Already downloaded.')
        return 1
    response = requests.get(f'https://shbabbek.com/natega/{seat_num}')
    soup = BeautifulSoup(response.content)

    valid = (soup.find(text='تأكد من رقم الجلوس')==None)

    if valid:
        print('Valid')
        with open(PAGES_PATH+f'{seat_num}.html', 'wb') as f:
            f.write(response.content)
    else:
        print('Invalid')
    return 0


if __name__ == '__main__':
    print('High School Results Downloader using Threading')
    print('By: Aly Eyad')

    print('Seat Numbers range from 102300 to 937412')
    start = int(input("Enter the start of the range: "))
    finish = int(input("Enter the end of the range: ")) + 1
    if not os.path.exists('./student_pages'):
        os.makedirs('./student_pages')
    s_num_range = list(range(start,finish))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(check_seat_num, s_num_range)
