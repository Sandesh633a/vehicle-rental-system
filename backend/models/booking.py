# import extensions
# from bson import ObjectId

# class BookingModel:

#     @staticmethod
#     def has_conflict(vehicle_id, start_time, end_time):
#         return extensions.db.bookings.find_one({
#             "vehicle_id": ObjectId(vehicle_id),
#             "status": "active",
#             "start_time": {"$lt": end_time},
#             "end_time": {"$gt": start_time}
#         }) is not None

#     @staticmethod
#     def create_booking(user_id, vehicle_id, start_time, end_time, total_cost):
#         booking = {
#             "user_id": ObjectId(user_id),
#             "vehicle_id": ObjectId(vehicle_id),
#             "start_time": start_time,
#             "end_time": end_time,
#             "total_cost": total_cost,
#             "status": "active"
#         }
#         return extensions.db.bookings.insert_one(booking)

#     @staticmethod
#     def cancel_booking(booking_id, user_id):
#         return extensions.db.bookings.update_one(
#             {
#                 "_id": ObjectId(booking_id),
#                 "user_id": ObjectId(user_id),
#                 "status": "active"
#             },
#             {"$set": {"status": "cancelled"}}
#         )


#     @staticmethod
#     def get_all_bookings():
#         return extensions.db.bookings.find()


















import extensions
from bson import ObjectId


class BookingModel:

    @staticmethod
    def has_conflict(vehicle_id, start_time, end_time):
        return extensions.db.bookings.find_one({
            "vehicle_id": ObjectId(vehicle_id),
            "status": "active",
            "start_time": {"$lt": end_time},
            "end_time": {"$gt": start_time}
        }) is not None

    @staticmethod
    def create_booking(user_id, vehicle_id, start_time, end_time, total_cost):
        booking = {
            "user_id": ObjectId(user_id),
            "vehicle_id": ObjectId(vehicle_id),
            "start_time": start_time,
            "end_time": end_time,
            "total_cost": total_cost,
            "status": "active"   # 🔥 IMPORTANT
        }
        return extensions.db.bookings.insert_one(booking)

    @staticmethod
    def cancel_booking(booking_id, user_id):
        return extensions.db.bookings.update_one(
            {
                "_id": ObjectId(booking_id),
                "user_id": ObjectId(user_id),
                "status": "active"
            },
            {
                "$set": {"status": "cancelled"}
            }
        )

    @staticmethod
    def get_all_bookings():
        return extensions.db.bookings.find()
