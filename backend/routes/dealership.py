from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.role_required import role_required
from models.dealership import DealershipModel

dealership_bp = Blueprint("dealership", __name__, url_prefix="/dealership")

@dealership_bp.route("/add", methods=["POST"])
@jwt_required()
@role_required("admin")
def add_dealership():
    data = request.json

    DealershipModel.create_dealership(
        name=data["name"],
        address=data["address"],
        latitude=data["latitude"],
        longitude=data["longitude"]
    )

    return jsonify({"message": "Dealership added successfully"}), 201