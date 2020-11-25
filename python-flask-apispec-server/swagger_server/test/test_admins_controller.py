# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inventory_item import InventoryItem  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAdminsController(BaseTestCase):
    """AdminsController integration test stubs"""

    def test_add_inventory(self):
        """Test case for add_inventory

        adds an inventory item
        """
        inventoryItem = InventoryItem()
        response = self.client.open(
            '/FinEst-Twins/test/1.0.0/inventory',
            method='POST',
            data=json.dumps(inventoryItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
