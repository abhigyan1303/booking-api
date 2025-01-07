# facade/bus_facade.py
import logging
from flask import current_app
from bson.objectid import ObjectId
from models.bus import Bus

class BusFacade:
    @staticmethod
    def create_bus(travel, isAc, isSleeper, registration, totalSeat, insuranceValidTill, permitValidTill, createdBy):
        try:
            bus = Bus(
                travel=travel,
                isAc=isAc,
                isSleeper=isSleeper,
                registration=registration,
                totalSeat=totalSeat,
                insuranceValidTill=insuranceValidTill,
                permitValidTill=permitValidTill,
                createdBy=createdBy
            )
            result = current_app.mongo.db.buses.insert_one(bus.to_dict())
            bus._id = str(result.inserted_id)
            return bus.to_dict()
        except Exception as e:
            logging.error("Error creating bus: %s", e)
            raise

    @staticmethod
    def get_bus(bus_id):
        try:
            bus_data = current_app.mongo.db.buses.find_one({"_id": ObjectId(bus_id)})
            if bus_data:
                bus = Bus.from_dict(bus_data)
                return bus.to_dict()
            return None
        except Exception as e:
            logging.error("Error getting bus: %s", e)
            raise

    @staticmethod
    def update_bus(bus_id, travel=None, isAc=None, isSleeper=None, registration=None, totalSeat=None, insuranceValidTill=None, permitValidTill=None, updatedAt=None):
        try:
            update_fields = {}
            if travel:
                update_fields["travel"] = travel
            if isAc is not None:
                update_fields["isAc"] = isAc
            if isSleeper is not None:
                update_fields["isSleeper"] = isSleeper
            if registration:
                update_fields["registration"] = registration
            if totalSeat:
                update_fields["totalSeat"] = totalSeat
            if insuranceValidTill:
                update_fields["insuranceValidTill"] = insuranceValidTill
            if permitValidTill:
                update_fields["permitValidTill"] = permitValidTill
            if updatedAt:
                update_fields["updatedAt"] = updatedAt
            result = current_app.mongo.db.buses.update_one(
                {"_id": ObjectId(bus_id)}, {"$set": update_fields}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error("Error updating bus: %s", e)
            raise

    @staticmethod
    def delete_bus(bus_id):
        try:
            result = current_app.mongo.db.buses.delete_one({"_id": ObjectId(bus_id)})
            return result.deleted_count > 0
        except Exception as e:
            logging.error("Error deleting bus: %s", e)
            raise

    @staticmethod
    def get_all_buses(page, size):
        try:
            skip = (page - 1) * size
            buses_cursor = current_app.mongo.db.buses.find().skip(skip).limit(size)
            buses = [Bus.from_dict(bus).to_dict() for bus in buses_cursor]
            total_buses = current_app.mongo.db.buses.count_documents({})
            return {
                "buses": buses,
                "pageSize": size,
                "currentPage": page,
                "totalData": total_buses
            }
        except Exception as e:
            logging.error("Error getting all buses: %s", e)
            raise