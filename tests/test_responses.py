from tests import TestMixin
import unittest
import json


class EndpointStatusCodes(TestMixin, unittest.TestCase):

    def test_home_status_code(self):
        result = self.app.get('/')

        self.assertEqual(result.status_code, 200)
