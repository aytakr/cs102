from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    id = request.query['id']
    label = request.query['label']
    s = session()
    news = s.query(News).get(id)
    news.label = label
    s.commit()

    redirect("/news")


@route("/update")
def update_news():
    news_list = get_news('https://news.ycombinator.com/newest', n_pages=34)
    s = session()
    for new_news in news_list:
        q = s.query(News).filter(News.title==new_news['title'],
                                 News.author==new_news['author'])

        if not s.query(q.exists()).scalar():
            news = News(title=new_news['title'],
                        author=new_news['author'],
                        url=new_news['url'],
                        comments=int(new_news['comments']),
                        points=int(new_news['points']))
            s.add(news)
            s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    pass

if __name__ == "__main__":
    run(host="localhost", port=8080)
