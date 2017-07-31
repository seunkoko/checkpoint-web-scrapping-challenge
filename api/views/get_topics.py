import requests

from bs4 import BeautifulSoup
from flask_restful import Resource

class GetTopicsResource(Resource):
    """
    Contains endpoint for getting available topics
    """

    def get(self):
        """
        To fetch topics
        """

        url = 'http://punchng.com/'
        get_request = requests.get(url)
        data = get_request.text
        soup = BeautifulSoup(data, "html.parser")

        topics = soup.find("ul", id="primary-menu"
                          ).findAll("li", class_="menu-item-type-taxonomy")

        response_array = []

        for topic in topics:
            topic_details = BeautifulSoup(topic.text, "html.parser")
            topic_url = topic.contents[0].get('href')
            topic_name = topic_details.contents[0]

            if '\n' in topic_name:
                topic_name = topic_name.split('\n')[0]

            data = {
                "topic": topic_name,
                "url": topic_url
            }

            response_array.append(data)

        return {"data": response_array}, 200