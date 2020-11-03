import requests
from bs4 import BeautifulSoup
import re


def pattern(t):
    pattern = '[\w]+'
    for i in t:
        result = re.findall(pattern, i, re.U)
        return result
def inreresting_articles(URL,KEYWORDS):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    for article in  soup.find_all('article',class_ = 'post'):
        title = article.find('a', class_='post__title_link')
        link = title.attrs.get('href')
        new_response = requests.get(link)
        soup2 = BeautifulSoup(new_response.text, 'html.parser')
        hub_link = soup2.find_all('a',class_ = 'hub-link')
        hub_link_text = list(map(lambda x: x.text.lower(), hub_link))
        article_title = soup2.find_all('span', class_ = 'post__title-text')
        article_title_text = pattern(list(map(lambda x: x.text.lower(), article_title)))
        article_info = soup2.find_all('div', class_ = 'post__body_full')
        article_info_text = pattern(list(map(lambda x: x.text.lower(), article_info)))
        article_list = list()
        for word in KEYWORDS:
            if word in hub_link_text or word in article_title_text or word in article_info_text:
                title = article.find('a', class_ = 'post__title_link')
                title_text = title.text
                date = article.find('span', class_ = 'post__time')
                date_text = date.text
                total = f'{date_text} - "{title_text}" - {link}'
                if total not in article_list:
                    article_list.append(total)
                    print(article_list)

if __name__ == '__main__':
    inreresting_articles('https://habr.com/ru/all/', ['дизайн', 'фото', 'web', 'python'])


