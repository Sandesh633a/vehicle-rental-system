from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from flask_jwt_extended import jwt_required, get_jwt


from models.user import UserModel

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if UserModel.find_by_email(data["email"]):
        return jsonify({"error": "User already exists"}), 400

    UserModel.create_user(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data.get("role", "user")
    )

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = UserModel.find_by_email(data["email"])

    if not user or not UserModel.verify_password(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={"role": user["role"]}
    )

    return jsonify({"access_token": token}), 200




@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    claims = get_jwt()
    return jsonify({
        "message": "Access granted",
        "role": claims["role"]
    }), 200
