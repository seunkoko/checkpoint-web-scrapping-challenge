from flask import request
from flask_restful import Resource

from api.helpers.scrape_data import ScrapeData
from api.helpers.get_articles import GetArticles
from api.helpers.utils import Utils

scrape_data = ScrapeData()
get_articles = GetArticles()
utils = Utils()


class ArticlesByTopicResource(Resource):
    """
    Contains endpoint for getting articles by topic
    and searching articles
    """

    def get(self):
        """
        To fetch articles for a topic and search for articles
        """

        URL = 'http://punchng.com'

        # checks if the request does not contain topic, query or date
        if ("topic" not in request.args) and (
            "q" not in request.args) and (
            "date") not in request.args:
            return {
                "error": "Invalid url",
                "message": "No topic or query specified in the url "
                           "(api/v1/articles?topic=<topic_name>) or "
                           "(api/v1/articles?q=<query>)"
            }, 400

        # handles when the request has parameter topic
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

            # handles when there is date in the request parameter
            if "date" in request.args:
                URL = '{}/topics/{}'.format(URL, topic.lower())
                max_page_number = utils.get_max_page_number(URL)
                converted_date = utils.convert_date(request.args["date"])
                return {"message": request.args["date"],
                        "max_number": max_page_number}

            # checks if page number is specified in the url
            if "page" in request.args:
                page_number = request.args["page"]

                if page_number == "1":
                    URL = '{}/topics/{}'.format(URL, topic.lower())
                else:
                    URL = '{}/topics/{}/page/{}'.format(
                        URL, topic.lower(), page_number)
            else:
                URL = '{}/topics/{}'.format(URL, topic.lower())

        # handles when the request has parameter q (query)
        if "q" in request.args:
            search_query = request.args["q"]

            # checks if page number is specified in the url
            if "page" in request.args:
                page_number = request.args["page"]

                if page_number == "1":
                    URL = '{}/?s={}'.format(URL, search_query)
                else:
                    URL = '{}/page/{}/?s={}'.format(URL, page_number
                        , search_query)
            else:
                URL = '{}/?s={}'.format(URL, search_query)

        data = scrape_data.make_url_request(URL)
        soup = scrape_data.get_soup(data)

        articles = soup.findAll("div", class_="items col-sm-12")

        response_array = get_articles.get_all_articles(articles, request.args)

        if len(response_array) == 0:
            response_string = "No data available on that page"
            return {"data": response_string}, 200
        else:
            return {"data": response_array}, 200