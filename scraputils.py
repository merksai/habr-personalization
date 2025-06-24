import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    for article in parser.find_all('article'):
        author = article.find(class_='tm-user-info__username')
        if not author:
            continue

        complexity = article.find(class_='tm-article-complexity__label')
        complexity = complexity.text if complexity else ''

        news_list.append(
            {
                'author': author.text,
                'complexity': complexity,
                'id': article.get('id'),
                'link': 'https://habr.com' + article.find(class_='tm-title__link').get('href'),
                'title': article.find(class_='tm-title__link').text
            }
        )

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.find(attrs={'data-test-id': 'pagination-next-page'}).get('href')


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://habr.com" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news