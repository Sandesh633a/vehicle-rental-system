from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId

import extensions
from utils.role_required import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =========================
# ADMIN DASHBOARD (TEST)
# =========================
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@role_required("admin")
def admin_dashboard():
    return jsonify({
        "message": "Welcome Admin"
    }), 200


# =========================
# VIEW ALL BOOKINGS (ADMIN)
# =========================
@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
@role_required("admin")
def view_all_bookings():
    bookings = extensions.db.bookings.find()

    result = []
    for b in bookings:
        result.append({
            "booking_id": str(b["_id"]),
            "user_id": str(b["user_id"]),
            "vehicle_id": str(b["vehicle_id"]),
            "start_time": b["start_time"].isoformat(),
            "end_time": b["end_time"].isoformat(),
            "total_cost": b["total_cost"],
            "status": b.get("status", "active")
        })

    return jsonify(result), 200


# =========================
# TOTAL REVENUE (ADMIN)
# =========================
@admin_bp.route("/revenue", methods=["GET"])
@jwt_required()
@role_required("admin")
def total_revenue():
    pipeline = [
        {"$match": {"status": "active"}},
        {"$group": {
            "_id": None,
            "total_revenue": {"$sum": "$total_cost"},
            "total_bookings": {"$sum": 1}
        }}
    ]

    result = list(extensions.db.bookings.aggregate(pipeline))

    if not result:
        return jsonify({
            "total_revenue": 0,
            "total_bookings": 0
        }), 200

    return jsonify({
        "total_revenue": result[0]["total_revenue"],
        "total_bookings": result[0]["total_bookings"]
    }), 200


# =========================
# REVENUE PER VEHICLE (ADMIN)
# =========================
@admin_bp.route("/revenue/vehicles", methods=["GET"])
@jwt_required()
@role_required("admin")
def revenue_per_vehicle():
    pipeline = [
        {"$match": {"status": "active"}},
        {"$group": {
            "_id": "$vehicle_id",
            "revenue": {"$sum": "$total_cost"},
            "bookings": {"$sum": 1}
        }}
    ]

    result = []
    for r in extensions.db.bookings.aggregate(pipeline):
        result.append({
            "vehicle_id": str(r["_id"]),
            "revenue": r["revenue"],
            "bookings": r["bookings"]
        })

    return jsonify(result), 200
