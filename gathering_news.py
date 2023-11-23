from dotenv import dotenv_values

import requests
from bs4 import BeautifulSoup
import deepl

config = dotenv_values("./dist/.env")
DEEPL_AUTH_KEY = config.get("DEEPL_AUTH_KEY")

translator = deepl.Translator(DEEPL_AUTH_KEY) # type: ignore

def scrape_news(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    news_articles = []
    article_tags = soup.find_all('a', {'class': 'post-block__title__link'})
    for tag in article_tags:
        title = tag.text
        jp_title = translator.translate_text(title, target_lang="JA")
        link = tag['href']
        news_articles.append({'title': jp_title, 'link': link})

    return news_articles

if __name__ == "__main__":
    url = "https://techcrunch.com/"

    news_articles = scrape_news(url)

    # 抽出したニュースを表示
    if news_articles:
        for article in news_articles:
            print(f"Title: {article['title']}")
            print(f"Link: {article['link']}")
            print("------------------------")
