import json

from test.base import BaseTestCase

class ArticlesByTopicTestCase(BaseTestCase):
    """
    Tests the endpoint
    /api/v1/articles?topic=<topic_name>&page=<page_number>
    """

    def test_topic_not_in_request(self):
        """
        Tests when the topic is not a parameter in the url
        """

        res = self.client.get('/api/v1/articles')
        expected_response = {
            "error": "Invalid url",
            "message": "No topic specified in the url "
                        "(api/v1/articles?topic=<topic_name>)"
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
        Tests appropraite response when topic is valid
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

    def test_page_number_in_request(self):
        """
        Tests when page number is supplied as a parameter
        """

        res = self.client.get('/api/v1/articles?topic=news&page=3')
        generated_response = json.loads(res.data)
        generated_content = generated_response["data"][0]

        self.assertEqual(res.status_code, 200)
        self.assertIn("data", generated_response)
        self.assert_(generated_content["published_date"])
        self.assert_(generated_content["title"])
        self.assert_(generated_content["content"])
        self.assert_(generated_content["url"])
        self.assert_(generated_content["url_to_image"])

    def test_invalid_page_number(self):
        """
        Tests when an invalid page number is supplied
        """

        res = self.client.get('/api/v1/articles?topic=news&page=200000')
        expected_response = {
            "data": "No data available on page 200000"
        }
        generated_response = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn("data", generated_response)
        self.assertDictEqual(expected_response, generated_response)


