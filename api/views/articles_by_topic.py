import requests

from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource


class ArticlesByTopicResource(Resource):
    """
    Contains endpoint for getting articles by topic
    and searching articles
    """

    def get(self):
        """
        To fetch articles for a topic and search for articles
        """

        if "topic" in request.args:
            # expected topics
            topics = ["news", "sports", 'metro plus', "politics", "business",
                  "entertainment", "opinion", "editorial", "columnists",
                  "jobs", "airtime plus"]

            # checks if the topic is valid
            if request.args["topic"].lower() not in topics:
                return {
                "error": "Invalid topic",
                "message": "The topic name is invalid, check available "
                           "topics (api/v1/topics)"
            }, 400

            # replaces empty space in topic by '-'
            if ' ' in request.args["topic"]:
                topic = request.args["topic"].replace(' ', '-')
            else:
                topic = request.args["topic"]
            
            # checks if page number is specified in the url
            if "page" in request.args:
                page_number = request.args["page"]

                if page_number == "1":
                    url = 'http://punchng.com/topics/%s' % (topic.lower())
                else:
                    url = 'http://punchng.com/topics/%s/page/%s'% (topic.lower()
                        , page_number)
            else:
                url = 'http://punchng.com/topics/%s' % (topic.lower())
        elif "q" in request.args:
            search_query = request.args["q"]

            # checks if page number is specified in the url
            if "page" in request.args:
                page_number = request.args["page"]

                if page_number == "1":
                    url = 'http://punchng.com/?s=%s' % (search_query)
                else:
                    url = 'http://punchng.com/page/%s/?s=%s'% (page_number
                        , search_query)
            else:
                url = 'http://punchng.com/?s=%s' % (search_query)
        else:
            return {
                "error": "Invalid url",
                "message": "No topic or query specified in the url "
                           "(api/v1/articles?topic=<topic_name>) or "
                           "(api/v1/articles?q=<query>)"
            }, 400

        get_request = requests.get(url)
        data = get_request.text
        soup = BeautifulSoup(data, "html.parser")

        articles = soup.findAll("div", class_="items col-sm-12")

        response_array = []

        for article in articles:
            # print(article)
            aritcle = BeautifulSoup(article.text, "html.parser")

            if "topic" in request.args:
                fetch_published_date = article.find(
                                        "span", class_="pull-right")
                published_date = fetch_published_date.contents[0]
            else:
                fetch_published_date = article.find("div", class_="seg-time")
                published_date = fetch_published_date.contents[0].replace(
                                 '\t', '').replace('\r', '').replace('\n', '')
            
            fetch_title = article.find("h2", class_="seg-title")
            fetch_content = article.find("div",
                            class_="seg-summary").find("p")
            fetch_url = article.find('a')
            fetch_url_to_image = article.find("div", class_="blurry")

            title = fetch_title.contents[0]
            content = fetch_content.contents[0]
            url = fetch_url.get('href')
            url_to_image = fetch_url_to_image.get('style').split("'")[1]

            data = {
                "published_date": published_date,
                "title": title,
                "content": content,
                "url": url,
                "url_to_image": url_to_image
            }

            response_array.append(data)

        if len(response_array) == 0:
            response_string = "No data available on that page"
            return {"data": response_string}, 200
        else:
            return {"data": response_array}, 200
