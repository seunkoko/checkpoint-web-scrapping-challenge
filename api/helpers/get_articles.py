from .scrape_data import ScrapeData


class GetArticles(object):
    """
    Gets the articles from generated soup
    """

    def get_all_articles(self, articles, query):
        """
        Loops through the articles to retrieve each
        article
        """
        response_array = []
        
        for article in articles:
            aritcle = ScrapeData().get_soup(article.text)

            if "topic" in query:
                fetch_published_date = article.find(
                                        "span", class_="pull-right")
                published_date = self.verify_ariticle_key(
                                 fetch_published_date, False, False, False)
            else:
                fetch_published_date = article.find("div", class_="seg-time")
                published_date = self.verify_ariticle_key(fetch_published_date,
                            True, False, False)
            
            fetch_title = article.find("h2", class_="seg-title")
            fetch_content = article.find("div",
                            class_="seg-summary").find("p")
            fetch_url = article.find('a')
            fetch_url_to_image = article.find("div", class_="blurry")

            title = self.verify_ariticle_key(fetch_title, False, False,
                    False)
            content = self.verify_ariticle_key(fetch_content, False,
                        False, False)
            url = self.verify_ariticle_key(fetch_url, False, True,
                    False)
            url_to_image = self.verify_ariticle_key(fetch_url_to_image, False,
                            False, True)

            data = {
                "published_date": published_date,
                "title": title,
                "content": content,
                "url": url,
                "url_to_image": url_to_image
            }

            response_array.append(data)

        return response_array

    def verify_ariticle_key(self, key, regex, link, style):
        """
        Checks if a key is present in an article
        """
        if not key:
            return []
        elif regex:
            return key.contents[0].replace(
                '\t', '').replace('\r', '').replace('\n', '')
        elif link:
            return key.get('href')
        elif style:
            return key.get('style').split("'")[1]
        else:
            return key.contents[0]


