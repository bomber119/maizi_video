import re
import requests
from bs4 import BeautifulSoup

def getVideoUrl(lesson_url):
    res = requests.get(lesson_url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.content, "html.parser").get_text()
    pattern = re.compile(r'lessonUrl = "(.*?)".*', re.MULTILINE | re.DOTALL)
    video_url = pattern.search(soup).group(1)
    print(video_url)
    return video_url


def getLessonUrl(lesson_url):
    base_url = "http://www.maiziedu.com"
    url = base_url + lesson_url
    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.content, "html.parser")
    lesson_name = soup.find('span', attrs={'class': 'lesson_name'}).text
    lessons_list = []
    lessons = soup.find('div', attrs={'class': 'lesson'}).findAll('li')
    print('Total: ' + str(len(lessons)) + ' lessons')
    for lesson in lessons:
        try:
            name = lesson.find('a')['name']
            lesson_url = base_url+lesson.find('a')['href']
            video_url = getVideoUrl(lesson_url)
            row = {"name": name, "lesson_url": lesson_url, "video_url": video_url}
            lessons_list.append(row)
        except TypeError:
            name = lesson.find('span')['name']
            lesson_url = base_url+lesson.find('span')['href']
            video_url = getVideoUrl(lesson_url)
            row = {"name": name, "lesson_url": lesson_url, "video_url": video_url}
            lessons_list.append(row)
    return lesson_name, lessons_list


lessons_url = "/course/574-8147/"
data = getLessonUrl(lessons_url)
name = data[0]
video = data[1]

with open('url_txt/' + name + '.txt', 'w') as f:
    for url in video:
        f.write(url["video_url"]+'\n')
f.close()
