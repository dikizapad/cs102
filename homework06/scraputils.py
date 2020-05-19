import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    posts = parser.find('table', {"class": "itemlist"}).findAllNext('tr', {"class": "athing"})
    for post in posts:
        title = post.findNext('a', {"class": "storylink"}).text
        link = post.findNext('a', {"class": "storylink"}).attrs['href']
        author = post.findNext('td', {"class": "subtext"}).find('a').text
        points = post.findNext('td', {"class": "subtext"}).find('span').text
        points = int(points.split()[0])
        comments = post.findNext('td', {"class": "subtext"}).findAll('a')
        if len(comments) > 2:
            comments = post.findNext('td', {"class": "subtext"}).findAll('a')[3].text

            if comments == "discuss":
                comments = 0
            else:
                comments = int(comments.split()[0])
        else:
            comments = 0

        news = {"title": title, "link": link, "author": author, "points": points, "comments": comments}
        news_list.append(news)
    return news_list


def get_news(url="https://news.ycombinator.com/?p=", n_pages=2):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url + str(n_pages)))
        response = requests.get(url + str(n_pages))
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        news.extend(news_list)
        n_pages -= 1
    return news
