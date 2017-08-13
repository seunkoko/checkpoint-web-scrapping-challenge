class OpitimizeSearch(object):
    """
    It optimizes search between pages
    """
    def search_pages(self, url, upper_bound, date):
        lower_bound = 1
        page_found = None

        while page_found is None:
            if upper_bound < lower_bound:
                return False

            mid_point = lower_bound + ( upper_bound - lower_bound ) / 2

