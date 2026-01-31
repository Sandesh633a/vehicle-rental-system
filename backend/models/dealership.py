import extensions

class DealershipModel:
    @staticmethod
    def create_dealership(name, address, latitude, longitude):
        dealership = {
            "name": name,
            "address": address,
            "latitude": latitude,
            "longitude": longitude
        }
        return extensions.db.dealerships.insert_one(dealership)

    @staticmethod
    def get_all():
        return list(extensions.db.dealerships.find({}, {"_id": 0}))