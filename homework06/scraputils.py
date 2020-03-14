import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    soup = parser

    for i in range(30):
        title = soup.findAll('a', attrs={'class': 'storylink'})[i].text
        url = soup.findAll('a', attrs={'class': 'storylink'})[i]['href']
        points = soup.findAll('span', attrs={'class': 'score'})[i].text

        if points.count('points'):
            points = points.replace(' points', '')
        elif points.count('point'):
            points = points.replace(' point', '')
        else:
            points = '0'

        author = soup.findAll('a', attrs={'class': 'hnuser'})[i].text

        comments = soup.findAll('td', attrs={'class': 'subtext'})[i].findAll('a')[-1].text
        if len(comments.split()) == 1:
            comments = 0
        else:
            comments = comments.split()[0]

        s = {'author': author,
             'comments': comments,
             'points': points,
             'title': title,
             'url': url}

        news_list.append(s)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    next_page = ''
    for tag_a in parser.find_all('a'):
        if tag_a['href'].startswith('newest?'):
            next_page = tag_a['href']

    return next_page


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    n = 1
    while n <= n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser").table
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        #n_pages -= 1
        n += 1
    return news
