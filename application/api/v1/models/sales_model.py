from ..utils import get_item_by_key, get_all

SALES_DICT = []


class Sale():

    def put(self, sale_id, date_created, created_by, items_count, total_amount):
        self.onesale_dict = {}
        self.onesale_dict["sale_id"] = sale_id
        self.onesale_dict["date_created"] = date_created
        self.onesale_dict["created_by"] = created_by
        self.onesale_dict["items_count"] = items_count
        self.onesale_dict["total_amount"] = total_amount

        SALES_DICT.append(self.onesale_dict)
        return {"message": "A sale has been created successfully"}

    def get_all_sales(self):
        result = get_all(SALES_DICT)
        return result

    def get_sale_by_id(self, sale_id):
        result = get_item_by_key('sale_id', sale_id, SALES_DICT)
        return result
