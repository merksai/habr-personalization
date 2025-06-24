from bottle import (
    route, run, template, request, redirect, url, TemplateError
)

from scraputils import get_news
from db import News, session, select
from bayes import NaiveBayesClassifier


@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    id = int(request.query.id)

    s = session()
    news = s.query(News).get(id)
    news.label = label
    s.commit()

    if __name__ == "__main__":
        redirect('/news')


@route("/update_news")
def update_news():
    s = session()

    items = get_news("https://habr.com/ru/articles/", n_pages=5)
    for item in items:
        exists = s.query(News).filter(
            (News.title == item["title"]) & (News.author == item["author"])
        ).first()
        if not exists:
            news_obj = News(
                title=item["title"],
                author=item["author"],
                url=item["url"],
                complexity=item["complexity"],
                habr_id=item.get("id", None),
            )
            s.add(news_obj)
            s.commit()

    if __name__ == "__main__":
        redirect('/news')


def get_classification_list():
    s = session()
    marked_rows = s.query(News).filter(News.label != None).all()
    not_marked_rows = s.query(News).filter(News.label == None).all()

    X_train = [item.title for item in marked_rows]
    y_train = [item.label for item in marked_rows]
    X_predict = [item.title for item in not_marked_rows]

    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_predict)

    rows = list(zip(not_marked_rows, preds))
    rows_sorted = sorted(rows, key=lambda pair: pair[1])

    return [pair[0] for pair in rows_sorted]


@route("/classify")
def classify_news():
    return get_classification_list()


@route("/classify_page")
def classify_page():
    rows_for_template = []
    s = session()
    marked_rows = s.query(News).filter(News.label != None).all()
    not_marked_rows = s.query(News).filter(News.label == None).all()

    X_train = [item.title for item in marked_rows]
    y_train = [item.label for item in marked_rows]
    X_predict = [item.title for item in not_marked_rows]

    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_predict)

    rows = list(zip(not_marked_rows, preds))
    rows_sorted = sorted(rows, key=lambda pair: pair[1])
    
    return template("classify_template", rows=rows_sorted)

if __name__ == "__main__":
    run(host="localhost", port=8080)
