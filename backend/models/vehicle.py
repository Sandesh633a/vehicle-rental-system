import extensions
from bson import ObjectId

class VehicleModel:
    @staticmethod
    def add_vehicle(dealership_id, vehicle_type, model, rate_per_km):
        vehicle = {
            "dealership_id": ObjectId(dealership_id),
            "type": vehicle_type,
            "model": model,
            "rate_per_km": rate_per_km,
            "available": True
        }
        return extensions.db.vehicles.insert_one(vehicle)

    @staticmethod
    def get_available_vehicles():
        vehicles = extensions.db.vehicles.find({"available": True})

        result = []
        for v in vehicles:
            result.append({
                "id": str(v["_id"]),
                "dealership_id": str(v["dealership_id"]),
                "type": v["type"],
                "model": v["model"],
                "rate_per_km": v["rate_per_km"],
                "available": v["available"]
            })

        return result
    



    @staticmethod
    def is_available(vehicle_id, start_time, end_time):
        conflict = extensions.db.bookings.find_one({
            "vehicle_id": ObjectId(vehicle_id),
            "status": "active",
            "start_time": {"$lt": end_time},
            "end_time": {"$gt": start_time}
        })
        return conflict is None