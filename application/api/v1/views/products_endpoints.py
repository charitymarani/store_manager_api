
from flask import Flask, request, jsonify,Blueprint,json
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_claims)
from ..models import product_model

product = Blueprint('product', __name__,url_prefix='/api/v1')


product_object = product_model.Product()

@product.route('/products',methods=['POST'])
@jwt_required
def post_product():
    data=request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"}) 
    id=data.get("id")
    name=data.get("name")
    category=data.get("category")
    B_price=data.get("purchase_price")
    S_price=data.get("selling_price")
    qty=data.get("quantity")
    limit=data.get("low_limit")
    desc=data.get("description")

    if id is None or not id:
        return jsonify({"message": "Please specify the product id"}) 
    if name is None or not name:
        return jsonify({"message":"Enter the product name"}),206
    if qty is None or not qty:
        return jsonify({"message":"You must specify the quantity"}),206
    if limit is None or not limit:
        return jsonify({"message":"You must specify the low inventory limit"}),206
    if S_price is None or not S_price:
        return jsonify({"message":"You must specify the product price"}),206
    claims=get_jwt_claims()
    admin="admin"
    if claims['role'] != admin:
        return jsonify({"message":"Only an admin is permitted to post products"}),401
    response=jsonify(product_object.put(id, name, category, B_price,S_price,qty,limit,desc))

    response.status_code = 201
    return response  
@product.route('/products',methods=['GET']) 
@jwt_required
def get_all_products():
    response=jsonify(product_object.get_all_products())
    response.status_code=200
    return response
@product.route('/products/<product_id>',methods=['GET']) 
@jwt_required
def get_product_by_id(product_id):
    response=jsonify(product_object.get_product_by_id(product_id))
    response.status_code=200
    return response
