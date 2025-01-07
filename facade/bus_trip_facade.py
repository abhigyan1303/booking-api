# facade/bus_trip_facade.py
import logging
from flask import current_app
from bson.objectid import ObjectId
from models.bus_trip import BusTrip

class BusTripFacade:
    @staticmethod
    def create_trip(routeId, date, frequency, timing, fare, stops, createdBy):
        try:
            bus_trip = BusTrip(
                routeId=routeId,
                date=date,
                frequency=frequency,
                timing=timing,
                fare=fare,
                stops=stops,
                createdBy=createdBy
            )
            result = current_app.mongo.db.bus_trips.insert_one(bus_trip.to_dict())
            bus_trip._id = str(result.inserted_id)
            return bus_trip.to_dict()
        except Exception as e:
            logging.error("Error creating bus trip: %s", e)
            raise

    @staticmethod
    def get_trip(trip_id):
        try:
            trip_data = current_app.mongo.db.bus_trips.find_one({"_id": ObjectId(trip_id)})
            if trip_data:
                bus_trip = BusTrip.from_dict(trip_data)
                return bus_trip.to_dict()
            return None
        except Exception as e:
            logging.error("Error getting bus trip: %s", e)
            raise

    @staticmethod
    def update_trip(trip_id, routeId=None, date=None, frequency=None, timing=None, fare=None, stops=None, updatedAt=None):
        try:
            update_fields = {}
            if routeId:
                update_fields["routeId"] = routeId
            if date:
                update_fields["date"] = date
            if frequency:
                update_fields["frequency"] = frequency
            if timing:
                update_fields["timing"] = timing
            if fare is not None:
                update_fields["fare"] = fare
            if stops:
                update_fields["stops"] = stops
            if updatedAt:
                update_fields["updatedAt"] = updatedAt
            result = current_app.mongo.db.bus_trips.update_one(
                {"_id": ObjectId(trip_id)}, {"$set": update_fields}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error("Error updating bus trip: %s", e)
            raise

    @staticmethod
    def delete_trip(trip_id):
        try:
            result = current_app.mongo.db.bus_trips.delete_one({"_id": ObjectId(trip_id)})
            return result.deleted_count > 0
        except Exception as e:
            logging.error("Error deleting bus trip: %s", e)
            raise

    @staticmethod
    def get_all_trips(page, size, date=None, busTypes=None, from_city=None, to_city=None):
        try:
            query = {}
            if date:
                query['date'] = date
            if busTypes:
                query['busTypes'] = busTypes
            if from_city:
                query['from'] = from_city
            if to_city:
                query['to'] = to_city

            skip = (page - 1) * size
            trips_cursor = current_app.mongo.db.bus_trips.find(query).skip(skip).limit(size)
            trips = [BusTrip.from_dict(trip).to_dict() for trip in trips_cursor]
            total_trips = current_app.mongo.db.bus_trips.count_documents(query)
            return {'trips': trips, 'total': total_trips}
        except Exception as e:
            logging.error("Error getting bus trips: %s", e)
            raise