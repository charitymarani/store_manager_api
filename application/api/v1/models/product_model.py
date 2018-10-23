from ..utils import get_item_by_key, get_all

PRODUCTS_LIST = []


class Product():

    def put(self, product_id, name, category, purchase_price, selling_price, quantity, low_limit, description):
        self.oneproduct_dict = {}
        product_data = get_item_by_key('product_id', product_id, PRODUCTS_LIST)
        if "message" not in product_data:
            return {"message": "The product Id you entered is being used for another product"}
        self.oneproduct_dict["product_id"] = product_id
        self.oneproduct_dict["name"] = name
        self.oneproduct_dict["category"] = category
        self.oneproduct_dict["purchase_price"] = purchase_price
        self.oneproduct_dict["selling_price"] = selling_price
        self.oneproduct_dict["quantity"] = quantity
        self.oneproduct_dict["low_limit"] = low_limit
        self.oneproduct_dict["description"] = description

        PRODUCTS_LIST.append(self.oneproduct_dict)
        return {"message": "Product with id {} added successfully".format(product_id)}

    def get_all_products(self):
        result = get_all(PRODUCTS_LIST)
        return result

    def get_product_by_id(self, product_id):
        result = get_item_by_key('product_id', product_id, PRODUCTS_LIST)
        return result
