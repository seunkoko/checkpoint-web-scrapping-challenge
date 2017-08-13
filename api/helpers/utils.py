from datetime import datetime

from .scrape_data import ScrapeData

class Utils(object):
    """
    Utilities
    """
    def get_max_page_number(self, url):
        """
        Gets the maximum page of a topic
        """
        data = ScrapeData().make_url_request(url)
        soup = ScrapeData().get_soup(data)
        pages = soup.findAll("a", class_="page-numbers")
        return int(pages[2].text.replace(',', ''))

    def convert_date(self, date):
        date_list = date.split(' ')
        date_string = "{} {} {}".format(
            date_list[0][0:3],
            date_list[1][0:1],
            date_list[2])
        return datetime.strptime(date_string, "%b %d %Y")    
