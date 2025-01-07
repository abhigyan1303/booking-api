# models/booking.py
from datetime import datetime, timezone


class Booking:
    def __init__(self, tripId, userId, seatNumber, status, createdAt=None, updatedAt=None, _id=None):
        self.tripId = tripId
        self.userId = userId
        self.seatNumber = seatNumber
        self.status = status
        self.createdAt = createdAt if createdAt else datetime.now(timezone.utc)
        self.updatedAt = updatedAt if updatedAt else datetime.now(timezone.utc)
        self._id = str(_id) if _id else None

    def to_dict(self):
        booking_dict = {
            "tripId": self.tripId,
            "userId": self.userId,
            "seatNumber": self.seatNumber,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
        if self._id:
            booking_dict["_id"] = self._id
        return booking_dict

    @staticmethod
    def from_dict(data):
        return Booking(
            tripId=data.get("tripId"),
            userId=data.get("userId"),
            seatNumber=data.get("seatNumber"),
            status=data.get("status"),
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt"),
            _id=str(data.get("_id")) if data.get("_id") else None
        )
