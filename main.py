from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import termcolor
import time
import threading

from vimeo_downloader import Vimeo


def login(driver, username, password):
    driver.get('https://northbirds.com/users/sign_in?from=iframe')  
    driver.find_element(By.NAME, 'user[email]').send_keys(username)
    driver.find_element(By.NAME, 'user[password]').send_keys(password)
    driver.find_element(By.NAME, 'commit').click()

def convert_cookies_to_str(cookies):
    cookies_str = ''
    for cookie in cookies:
        cookies_str += cookie['name'] + '=' + cookie['value'] + '; '
    return cookies_str

def get_course_info(driver, save_folder='lesson', save_name='course_info.md'):
    chapters = driver.find_element(By.ID, 'product-view')
    chapters = BeautifulSoup(chapters.get_attribute('innerHTML'), 'html.parser')
    course_info = pd.DataFrame(columns=['Lesson', 'Title', 'Time', 'URL'])
    for lesson in chapters.find_all('div', class_='item'):
        lesson_no = lesson.find(class_='lesson').text.strip()
        title = lesson.find(class_='item-title').text.strip().replace(' ', '')
        time = lesson.find(class_='time').text.strip()
        url = lesson.find('a')['href']
        info = pd.DataFrame({'Lesson': [lesson_no], 'Title': [f'[{title}]({save_folder}/{title}.mp4)'], 'Time': [time], 'URL': [url]})
        course_info = pd.concat([course_info, info], ignore_index=True)

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    with open(save_folder + '/' + save_name, 'w') as f:
        f.write('# ' + save_folder + '\n\n')
        f.write(course_info.to_markdown(index=False))
    return course_info

def download_video(vimeo_url, embedded_on, cookies, save_folder, file_name=None):
    v = Vimeo(vimeo_url, embedded_on, cookies=cookies)
    stream = v.streams
    stream[-1].download(save_folder, filename=file_name)

def multi_dload(course_info, embedded_on, cookies, save_folder):
    print('Downloading {} videos...'.format(len(course_info)))

    max_threads = threading.active_count() + 20
    threads = []
    for i in range(len(course_info)):
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        
        # if video exists, skip
        video_title = course_info['Title'][i].split('[')[1].split(']')[0]
        video_path = course_info['Title'][i].split('(')[1].split(')')[0]
        if os.path.exists(video_path):
            termcolor.cprint('Skipped ' + course_info['Title'][i], 'yellow')
            continue
        
        # else download video
        if threading.active_count() < max_threads:
            t = threading.Thread(target=download_video, args=(course_info['URL'][i], embedded_on, cookies, save_folder, video_title))
            t.start()
            threads.append(t)
        else:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()

    print('Finished downloading {} videos.'.format(len(course_info)))
    

for course_no in range(1, 24):

    driver = webdriver.Chrome()

    # login
    driver.get('https://northbirds.com/users/sign_in?from=iframe')
    login(driver, 'lulueven88@gmail.com', 'lulueven88')

    url = 'https://northbirds.com/courses/' + str(course_no)

    # get course title
    driver.get(url)
    page = BeautifulSoup(driver.page_source, 'html.parser')
    chapter_title = page.find('h2', class_='dropdown-title').text.strip()
    print(chapter_title)

    # get course info
    course_info = get_course_info(driver, save_folder= 'videos/' + chapter_title, save_name='README.md')

    # get cookies
    driver.find_element(By.ID, 'product-view').find_element(By.CLASS_NAME, 'item').find_element(By.TAG_NAME, 'a').click()
    cookie = convert_cookies_to_str(driver.get_cookies())
    driver.get('https://player.vimeo.com/')
    cookie += convert_cookies_to_str(driver.get_cookies())

    driver.quit()


    # download videos
    multi_dload(course_info, url, cookie, 'videos/' + chapter_title)
    
    # print('Downloading {} videos...'.format(len(course_info)))
    # for i in range(len(course_info)):
    #     if not os.path.exists(chapter_title):
    #         os.makedirs(chapter_title)
        
    #     # if video exists, skip
    #     title = course_info['Title'][i].split('(')[1].split(')')[0]
    #     if os.path.exists(chapter_title + '/' + title):
    #         termcolor.cprint('Skipped ' + course_info['Title'][i], 'yellow')
    #         continue
    #     # else download video
    #     download_video(course_info['URL'][i], url, cookie, chapter_title)
    #     termcolor.cprint('Downloaded ' + course_info['Title'][i], 'green')
    #     print('\n')

    # print('Finished downloading {} videos.'.format(len(course_info)))