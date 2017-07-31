import json

from test.base import BaseTestCase

class GetTopicsTestCase(BaseTestCase):
    """
    Tests the endpoint /api/v1/topics
    """

    def test_get_topics_api(self):
        """
        Tests appropriate response when the endpoint is hit
        """

        res = self.client.get('/api/v1/topics')
        generated_response = json.loads(res.data)
        generated_content = generated_response["data"][0]

        self.assertEqual(res.status_code, 200)
        self.assertIn("data", generated_response)
        self.assert_(generated_content["topic"])
        self.assert_(generated_content["url"])
