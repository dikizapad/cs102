from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session, add_to_db
from bayes import NaiveBayesClassifier

s = session()


@route("/news")
def news_list():
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    n_id = request.query.id
    news = s.query(News).filter(News.id == n_id).one()
    news.label = label
    s.add(news)
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news = get_news()
    rows = s.query(News).all()
    for n in news:
        flag = True
        for row in rows:
            if n['title'] == row.title:
                flag = False
                break
        if flag:
            add_to_db(n)

    redirect("/news")


@route("/classify")
def classify_news():
    rows = s.query(News).filter(News.label != None).all()
    a = NaiveBayesClassifier()
    name = []
    lables = []
    for n in rows:
        name.append(n.title)
        lables.append(n.label)
    a.fit(name, lables)
    rows = s.query(News).filter(News.label == None).all()
    for n in rows:
        name.append(n.title)
    result = a.predict(name)
    for num,n in enumerate(rows):
         n.label = result[num]
    return template('classify_template', rows=rows)



if __name__ == "__main__":
    run(host="localhost", port=8080)
