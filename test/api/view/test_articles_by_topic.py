import json

from test.base import BaseTestCase

class ArticlesByTopicTestCase(BaseTestCase):
    """
    Tests the endpoints
    /api/v1/articles?topic=<topic_name>&page=<page_number>
    /api/v1/articles?q=<query>&page=<page_number>
    """

    def test_topic_or_query__not_in_request(self):
        """
        Tests when the topic is not a parameter in the url
        """

        res = self.client.get('/api/v1/articles')
        expected_response = {
            "error": "Invalid url",
            "message": "No topic or query specified in the url "
                       "(api/v1/articles?topic=<topic_name>) or "
                       "(api/v1/articles?q=<query>)"
        }
        generated_response = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(generated_response['error'],
                         expected_response['error'])
        self.assertEqual(generated_response['message'],
                         expected_response['message'])

    def test_invalid_topic(self):
        """
        Tests when a topic is invalid
        """

        res = self.client.get('/api/v1/articles?topic=invalid')
        expected_response = {
            "error": "Invalid topic",
            "message": "The topic name is invalid, check available "
                        "topics (api/v1/topics)"
        }
        generated_response = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(generated_response['error'],
                         expected_response['error'])
        self.assertEqual(generated_response['message'],
                         expected_response['message'])

    def test_valid_topic(self):
        """
        Tests appropriate response when topic is valid
        """

        res = self.client.get('/api/v1/articles?topic=news')
        generated_response = json.loads(res.data)
        generated_content = generated_response["data"][0]

        self.assertEqual(res.status_code, 200)
        self.assertIn("data", generated_response)
        self.assert_(generated_content["published_date"])
        self.assert_(generated_content["title"])
        self.assert_(generated_content["content"])
        self.assert_(generated_content["url"])
        self.assert_(generated_content["url_to_image"])

    def test_valid_query(self):
        """
        Tests appropriate response when query is valid
        """

        res = self.client.get('/api/v1/articles?q=eye')
        generated_response = json.loads(res.data)
        generated_content = generated_response["data"][0]

        self.assertEqual(res.status_code, 200)
        self.assertIn("data", generated_response)
        self.assert_(generated_content["published_date"])
        self.assert_(generated_content["title"])
        self.assert_(generated_content["content"])
        self.assert_(generated_content["url"])
        self.assert_(generated_content["url_to_image"])

    def test_page_number_in_request(self):
        """
        Tests when page number is supplied as a parameter
        """

        res_topic = self.client.get('/api/v1/articles?topic=news&page=3')
        res_query = self.client.get('/api/v1/articles?q=eye&page=3')
        generated_response_topic = json.loads(res_topic.data)
        generated_content_topic = generated_response_topic["data"][0]
        generated_response_query = json.loads(res_query.data)
        generated_content_query = generated_response_query["data"][0]

        self.assertEqual(res_topic.status_code, 200)
        self.assertEqual(res_query.status_code, 200)
        self.assertIn("data", generated_response_topic)
        self.assertIn("data", generated_response_query)
        self.assert_(generated_content_topic["published_date"])
        self.assert_(generated_content_query["published_date"])
        self.assert_(generated_content_topic["title"])
        self.assert_(generated_content_query["title"])
        self.assert_(generated_content_topic["content"])
        self.assert_(generated_content_query["content"])
        self.assert_(generated_content_topic["url"])
        self.assert_(generated_content_query["url"])
        self.assert_(generated_content_topic["url_to_image"])
        self.assert_(generated_content_query["url_to_image"])

    def test_invalid_page_number(self):
        """
        Tests when an invalid page number is supplied
        """

        res_topic = self.client.get('/api/v1/articles?topic=news&page=200000')
        res_query = self.client.get('/api/v1/articles?q=eye&page=200000')
        expected_response = {
            "data": "No data available on that page"
        }
        generated_response_topic = json.loads(res_topic.data)
        generated_response_query = json.loads(res_query.data)

        self.assertEqual(res_topic.status_code, 200)
        self.assertEqual(res_query.status_code, 200)
        self.assertIn("data", generated_response_topic)
        self.assertDictEqual(expected_response, generated_response_query)


