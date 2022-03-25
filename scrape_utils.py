import requests
from bs4 import BeautifulSoup


def get_content(url):
    response = requests.get(url)
    print("STATUS_CODE:", response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find("h1", class_="article-title").text
    abstract = soup.find("h2", class_="sapo").text
    body = soup.find("div", id="main-detail-body")
    content = ' '.join(paragraph.text for paragraph in body.findChildren("p", recursive=False))
    article = {"title": title,
               "abstract": abstract,
               "body": body,
               "content": content,
               }

    return article["content"]

