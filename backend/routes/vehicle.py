from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.role_required import role_required
from models.vehicle import VehicleModel

vehicle_bp = Blueprint("vehicle", __name__, url_prefix="/vehicles")

@vehicle_bp.route("/add", methods=["POST"])
@jwt_required()
@role_required("admin")
def add_vehicle():
    data = request.json

    VehicleModel.add_vehicle(
        dealership_id=data["dealership_id"],
        vehicle_type=data["type"],
        model=data["model"],
        rate_per_km=data["rate_per_km"]
    )

    return jsonify({"message": "Vehicle added successfully"}), 201


@vehicle_bp.route("", methods=["GET"])
def get_vehicles():
    vehicles = VehicleModel.get_available_vehicles()
    return jsonify(vehicles), 200