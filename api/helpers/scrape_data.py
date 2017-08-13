import requests

from bs4 import BeautifulSoup

class ScrapeData(object):
    """
    Handles the scrapping of data from webpages
    """

    def make_url_request(self, url):
        """
        Makes a request to the url specified
        in order to get the webpage
        """

        get_request = requests.get(url)
        return get_request.text

    def get_soup(self, data):
        """
        Allows us to extract data out of HTML
        pages supplied
        """

        return BeautifulSoup(data, "html.parser")