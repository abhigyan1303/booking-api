# models/bus.py
from bson.objectid import ObjectId
from datetime import datetime, timezone

class Bus:
    def __init__(self, travel, isAc, isSleeper, registration, totalSeat, insuranceValidTill, permitValidTill, createdBy, createdAt=None, updatedAt=None, _id=None):
        self.travel = travel
        self.isAc = isAc
        self.isSleeper = isSleeper
        self.registration = registration
        self.totalSeat = totalSeat
        self.insuranceValidTill = insuranceValidTill
        self.permitValidTill = permitValidTill
        self.createdBy = createdBy
        self.createdAt = createdAt if createdAt else datetime.now(timezone.utc)
        self.updatedAt = updatedAt if updatedAt else datetime.now(timezone.utc)
        self._id = str(_id) if _id else None

    def to_dict(self):
        bus_dict = {
            "travel": self.travel,
            "isAc": self.isAc,
            "isSleeper": self.isSleeper,
            "registration": self.registration,
            "totalSeat": self.totalSeat,
            "insuranceValidTill": self.insuranceValidTill,
            "permitValidTill": self.permitValidTill,
            "createdBy": self.createdBy,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
        if self._id:
            bus_dict["_id"] = self._id
        return bus_dict

    @staticmethod
    def from_dict(data):
        return Bus(
            travel=data.get("travel"),
            isAc=data.get("isAc"),
            isSleeper=data.get("isSleeper"),
            registration=data.get("registration"),
            totalSeat=data.get("totalSeat"),
            insuranceValidTill=data.get("insuranceValidTill"),
            permitValidTill=data.get("permitValidTill"),
            createdBy=data.get("createdBy"),
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt"),
            _id=str(data.get("_id")) if data.get("_id") else None
        )
