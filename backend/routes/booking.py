# # backend/routes/booking.py

# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from datetime import datetime
# from bson import ObjectId

# from models.booking import BookingModel
# import extensions

# booking_bp = Blueprint("booking", __name__, url_prefix="/bookings")


# @booking_bp.route("/create", methods=["POST"])
# @jwt_required()
# def create_booking():
#     data = request.json
#     user_id = get_jwt_identity()

#     vehicle_id = data["vehicle_id"]
#     start_time = datetime.fromisoformat(data["start_time"])
#     end_time = datetime.fromisoformat(data["end_time"])

#     # 1️⃣ Validate time range
#     if end_time <= start_time:
#         return jsonify({"error": "Invalid time range"}), 400

#     # 2️⃣ Check booking conflict
#     if BookingModel.has_conflict(vehicle_id, start_time, end_time):
#         return jsonify({"error": "Vehicle already booked for this time"}), 409

#     # 3️⃣ Fetch vehicle rate from DB (SECURE)
#     vehicle = extensions.db.vehicles.find_one(
#         {"_id": ObjectId(vehicle_id)}
#     )

#     if not vehicle:
#         return jsonify({"error": "Vehicle not found"}), 404

#     rate = vehicle["rate_per_km"]

#     # 4️⃣ Cost calculation (hours based)
#     hours = (end_time - start_time).total_seconds() / 3600
#     total_cost = round(hours * rate, 2)

#     # 5️⃣ Create booking
#     BookingModel.create_booking(
#         user_id=user_id,
#         vehicle_id=vehicle_id,
#         start_time=start_time,
#         end_time=end_time,
#         total_cost=total_cost
#     )

#     return jsonify({
#         "message": "Booking confirmed",
#         "total_cost": total_cost
#     }), 201



# @booking_bp.route("/my", methods=["GET"])
# @jwt_required()
# def my_bookings():
#     user_id = get_jwt_identity()

#     bookings = extensions.db.bookings.find({
#         "user_id": ObjectId(user_id)
#     })

#     result = []
#     for b in bookings:
#         result.append({
#             "booking_id": str(b["_id"]),
#             "vehicle_id": str(b["vehicle_id"]),
#             "start_time": b["start_time"].isoformat(),
#             "end_time": b["end_time"].isoformat(),
#             "total_cost": b["total_cost"],
#             "status": b.get("status", "active")  # 🔥 SAFE FIX
#         })

#     return jsonify(result), 200





# @booking_bp.route("/cancel/<booking_id>", methods=["POST"])
# @jwt_required()
# def cancel_booking(booking_id):
#     user_id = get_jwt_identity()

#     result = BookingModel.cancel_booking(booking_id, user_id)

#     if result.matched_count == 0:
#         return jsonify({"error": "Booking not found or already cancelled"}), 404

#     return jsonify({"message": "Booking cancelled successfully"}), 200














from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId

import extensions
from models.booking import BookingModel
from models.vehicle import VehicleModel   # 🔥 availability logic

booking_bp = Blueprint("booking", __name__, url_prefix="/bookings")


# =========================
# CREATE BOOKING (USER)
# =========================
@booking_bp.route("/create", methods=["POST"])
@jwt_required()
def create_booking():
    data = request.json
    user_id = get_jwt_identity()

    vehicle_id = data["vehicle_id"]
    start_time = datetime.fromisoformat(data["start_time"])
    end_time = datetime.fromisoformat(data["end_time"])

    # 1️⃣ Validate time range
    if end_time <= start_time:
        return jsonify({"error": "Invalid time range"}), 400

    # 2️⃣ Availability check (PHASE 6 LOGIC)
    if not VehicleModel.is_available(vehicle_id, start_time, end_time):
        return jsonify({"error": "Vehicle not available for selected time"}), 409

    # 3️⃣ Fetch vehicle rate securely
    vehicle = extensions.db.vehicles.find_one({
        "_id": ObjectId(vehicle_id)
    })

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    rate = vehicle["rate_per_km"]

    # 4️⃣ Cost calculation (hours based)
    hours = (end_time - start_time).total_seconds() / 3600
    total_cost = round(hours * rate, 2)

    # 5️⃣ Create booking
    BookingModel.create_booking(
        user_id=user_id,
        vehicle_id=vehicle_id,
        start_time=start_time,
        end_time=end_time,
        total_cost=total_cost
    )

    return jsonify({
        "message": "Booking confirmed",
        "total_cost": total_cost
    }), 201


# =========================
# VIEW MY BOOKINGS (USER)
# =========================
@booking_bp.route("/my", methods=["GET"])
@jwt_required()
def my_bookings():
    user_id = get_jwt_identity()

    bookings = extensions.db.bookings.find({
        "user_id": ObjectId(user_id)
    })

    result = []
    for b in bookings:
        result.append({
            "booking_id": str(b["_id"]),
            "vehicle_id": str(b["vehicle_id"]),
            "start_time": b["start_time"].isoformat(),
            "end_time": b["end_time"].isoformat(),
            "total_cost": b["total_cost"],
            "status": b.get("status", "active")  # ✅ safe
        })

    return jsonify(result), 200


# =========================
# CANCEL BOOKING (USER)
# =========================
@booking_bp.route("/cancel/<booking_id>", methods=["POST"])
@jwt_required()
def cancel_booking(booking_id):
    user_id = get_jwt_identity()

    result = BookingModel.cancel_booking(booking_id, user_id)

    if result.matched_count == 0:
        return jsonify({"error": "Booking not found or already cancelled"}), 404

    return jsonify({"message": "Booking cancelled successfully"}), 200
