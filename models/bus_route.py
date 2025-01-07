# models/bus_route.py
from datetime import datetime, timezone

class BusRoute:
    def __init__(self, route, routeNo, distance, createdBy, createdAt=None, updatedAt=None, _id=None):
        self.route = route
        self.routeNo = routeNo
        self.distance = distance
        self.createdBy = createdBy
        self.createdAt = createdAt if createdAt else datetime.now(timezone.utc)
        self.updatedAt = updatedAt if updatedAt else datetime.now(timezone.utc)
        self._id = str(_id) if _id else None

    def to_dict(self):
        route_dict = {
            "route": self.route,
            "routeNo": self.routeNo,
            "distance": self.distance,
            "createdBy": self.createdBy,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
        if self._id:
            route_dict["_id"] = self._id
        return route_dict

    @staticmethod
    def from_dict(data):
        return BusRoute(
            route=data.get("route"),
            routeNo=data.get("routeNo"),
            distance=data.get("distance"),
            createdBy=data.get("createdBy"),
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt"),
            _id=str(data.get("_id")) if data.get("_id") else None
        )