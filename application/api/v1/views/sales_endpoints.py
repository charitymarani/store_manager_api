import datetime
from flask import Flask, request, jsonify,Blueprint,json
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims,get_jwt_identity)
from ..models import sales_model
from ..models.sales_model import SALES_DICT

sale = Blueprint('sale', __name__,url_prefix='/api/v1')


sale_object = sales_model.Sale()

@sale.route('/sales',methods=['POST'])
@jwt_required
def post_sales():
    data=request.get_json()
    item_count=data.get("items_count")
    total_amount=data.get("total_amount")
    created_by=get_jwt_identity()
    now = datetime.datetime.now()
    date_created=now
    sale_id=len(SALES_DICT)

    if item_count is None or not item_count:
        return jsonify({"message": "Enter the items count"}),206
    if total_amount is None or not total_amount:
        return jsonify({"message":"Enter total amount in this sale"}),206

    claims=get_jwt_claims()
    attendant="attendant"
    if claims["role"] != attendant:
        return jsonify({"message":"Only an attendant is permitted to post sales"}),401
    response=jsonify(sale_object.put(sale_id,date_created,created_by,item_count,total_amount))
    response.status_code=201
    return response

@sale.route('/sales',methods=['GET'])
@jwt_required
def get_all_sales():
    claims=get_jwt_claims()
    admin="admin"
    if claims["role"]!= admin:
        return jsonify({"message":"Only an admin can view all sales records"}),401
    response= jsonify(sale_object.get_all_sales())
    response.status_code=200
    return response



