from flask_restful import Resource

from api.helpers.scrape_data import ScrapeData

scrape_data = ScrapeData()

class GetTopicsResource(Resource):
    """
    Contains endpoint for getting available topics
    """

    def get(self):
        """
        To fetch topics
        """

        URL = 'http://punchng.com/'
        data = scrape_data.make_url_request(URL)
        soup = scrape_data.get_soup(data)

        topics = soup.find("ul", id="primary-menu"
                          ).findAll("li", class_="menu-item-type-taxonomy")

        response_array = []

        for topic in topics:
            topic_details = scrape_data.get_soup(topic.text)
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
