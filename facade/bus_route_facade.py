# facade/bus_route_facade.py
import logging
from flask import current_app
from bson.objectid import ObjectId
from models.bus_route import BusRoute

class BusRouteFacade:

    @staticmethod
    def add_city(name):
        try:
            city = {"name": name}
            result = current_app.mongo.db.cities.insert_one(city)
            city["_id"] = str(result.inserted_id)
            return city
        except Exception as e:
            logging.error("Error adding city: %s", e)
            raise

    @staticmethod
    def list_cities(query):
        try:
            cities_cursor = current_app.mongo.db.cities.find({"name": {"$regex": query, "$options": "i"}})
            cities = [{"_id": str(city["_id"]), "name": city["name"]} for city in cities_cursor]
            return cities
        except Exception as e:
            logging.error("Error listing cities: %s", e)
            raise
    @staticmethod
    def create_route(route, routeNo, distance, createdBy):
        try:
            bus_route = BusRoute(
                route=route,
                routeNo=routeNo,
                distance=distance,
                createdBy=createdBy
            )
            result = current_app.mongo.db.bus_routes.insert_one(bus_route.to_dict())
            bus_route._id = str(result.inserted_id)
            return bus_route.to_dict()
        except Exception as e:
            logging.error("Error creating bus route: %s", e)
            raise

    @staticmethod
    def get_route(route_id):
        try:
            route_data = current_app.mongo.db.bus_routes.find_one({"_id": ObjectId(route_id)})
            if route_data:
                bus_route = BusRoute.from_dict(route_data)
                return bus_route.to_dict()
            return None
        except Exception as e:
            logging.error("Error getting bus route: %s", e)
            raise

    @staticmethod
    def update_route(route_id, route=None, routeNo=None, distance=None, updatedAt=None):
        try:
            update_fields = {}
            if route:
                update_fields["route"] = route
            if routeNo is not None:
                update_fields["routeNo"] = routeNo
            if distance is not None:
                update_fields["distance"] = distance
            if updatedAt:
                update_fields["updatedAt"] = updatedAt
            result = current_app.mongo.db.bus_routes.update_one(
                {"_id": ObjectId(route_id)}, {"$set": update_fields}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error("Error updating bus route: %s", e)
            raise

    @staticmethod
    def delete_route(route_id):
        try:
            result = current_app.mongo.db.bus_routes.delete_one({"_id": ObjectId(route_id)})
            return result.deleted_count > 0
        except Exception as e:
            logging.error("Error deleting bus route: %s", e)
            raise

    @staticmethod
    def get_all_routes(page, size):
        try:
            skip = (page - 1) * size
            routes_cursor = current_app.mongo.db.bus_routes.find().skip(skip).limit(size)
            routes = [BusRoute.from_dict(route).to_dict() for route in routes_cursor]
            total_routes = current_app.mongo.db.bus_routes.count_documents({})
            return {
                "routes": routes,
                "pageSize": size,
                "currentPage": page,
                "totalData": total_routes
            }
        except Exception as e:
            logging.error("Error getting all bus routes: %s", e)
            raise