PRODUCTS_DICT={}
class Product():
    def __init__(self):
        self.oneproduct_dict={}
    def put(self,product_id,name,category,purchase_price,selling_price,quantity,low_limit,description):
        if product_id in PRODUCTS_DICT:
            return {"message":"The product Id you entered is being used for another product"}
        self.oneproduct_dict["id"]=product_id
        self.oneproduct_dict["name"]=name
        self.oneproduct_dict["category"]=category
        self.oneproduct_dict["purchase_price"]=purchase_price
        self.oneproduct_dict["selling_price"]=selling_price
        self.oneproduct_dict["quantity"]=quantity
        self.oneproduct_dict["low_limit"]=low_limit
        self.oneproduct_dict["description"]=description

        PRODUCTS_DICT[product_id]=self.oneproduct_dict
        return {"message":"Product with id {} added successfully".format(product_id)}
    def get_all_products(self):
        return PRODUCTS_DICT
    def get_product_by_id(self,product_id):
        if product_id in PRODUCTS_DICT:
            return PRODUCTS_DICT[product_id]
        return{"message":"The product you are looking for does not exist"}



