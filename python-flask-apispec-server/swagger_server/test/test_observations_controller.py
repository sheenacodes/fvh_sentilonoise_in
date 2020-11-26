# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.sensors import Sensors  # noqa: E501
from swagger_server.test import BaseTestCase


class TestObservationsController(BaseTestCase):
    """ObservationsController integration test stubs"""

    def test_cesva_v1_post(self):
        """Test case for cesva_v1_post

        adds noise observations to UoP
        """
        Sensors = Sensors()
        response = self.client.open(
            '/FinEst-Twins/sentilonoise/1.0.0/cesva/v1',
            method='POST',
            data=json.dumps(Sensors),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
