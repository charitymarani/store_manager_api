import json
from .base_test import BaseTestCase
class TestSales(BaseTestCase):

    def test_post_sales(self):
        with self.client:
            response = self.client.post(
                '/api/v1/sales',
                data=json.dumps(dict(
                    item_count=4,
                    total_amount=5000
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            self.assertEqual("Sale added successfully",response_data["message"])
            self.assertEqual(response.status_code, 201)

    def test_get_all_sales(self):
        with self.client:
            response = self.client.get(
                '/api/v1/sales')
            response_data = json.loads(response.data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(response.status_code, 200)
    def test_get_sale_by_id(self):
        with self.client:
            response = self.client.get(
                '/api/v1/sales/1')
            response_data = json.loads(response.data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(response.status_code, 200)
