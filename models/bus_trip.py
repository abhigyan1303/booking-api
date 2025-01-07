# models/bus_trip.py
from datetime import datetime, timezone

class BusTrip:
    def __init__(self, routeId, date, frequency, timing, fare, stops, createdBy, createdAt=None, updatedAt=None, _id=None):
        self.routeId = routeId
        self.date = date
        self.frequency = frequency
        self.timing = timing
        self.fare = fare
        self.stops = stops
        self.createdBy = createdBy
        self.createdAt = createdAt if createdAt else datetime.now(timezone.utc)
        self.updatedAt = updatedAt if updatedAt else datetime.now(timezone.utc)
        self._id = str(_id) if _id else None

    def to_dict(self):
        trip_dict = {
            "routeId": self.routeId,
            "date": self.date,
            "frequency": self.frequency,
            "timing": self.timing,
            "fare": self.fare,
            "stops": self.stops,
            "createdBy": self.createdBy,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
        if self._id:
            trip_dict["_id"] = self._id
        return trip_dict

    @staticmethod
    def from_dict(data):
        return BusTrip(
            routeId=data.get("routeId"),
            date=data.get("date"),
            frequency=data.get("frequency"),
            timing=data.get("timing"),
            fare=data.get("fare"),
            stops=data.get("stops"),
            createdBy=data.get("createdBy"),
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt"),
            _id=str(data.get("_id")) if data.get("_id") else None
        )