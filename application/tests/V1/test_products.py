import json
from base_test import BaseTestCase
class TestProducts(BaseTestCase):

    def test_post_product(self):
        with self.client:
            response = self.client.post(
                '/api/v1/products',
                data=json.dumps(dict(
                    product_id=100,
                    name='chunky heels',
                    category='shoes',
                    purchase_price=1000,
                    selling_price=1800,
                    quantity=70,
                    low_inventory_limit=10,
                    description='A wide based heel'

                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            self.assertEqual("Product added successfully",response_data["message"])
            self.assertEqual(response.status_code, 201)

    def test_get_all_products(self):
        with self.client:
            response = self.client.get(
                '/api/v1/products')
            response_data = json.loads(response.data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(response.status_code, 200)
    def test_get_product_by_id(self):
        with self.client:
            response = self.client.get(
                '/api/v1/products/100')
            response_data = json.loads(response.data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(response.status_code, 200)