# facade/booking_facade.py
import logging
from flask import current_app
from bson.objectid import ObjectId
from models.booking import Booking

class BookingFacade:
    @staticmethod
    def create_booking(tripId, userId, seatNumber, status):
        try:
            booking = Booking(
                tripId=tripId,
                userId=userId,
                seatNumber=seatNumber,
                status=status
            )
            result = current_app.mongo.db.bookings.insert_one(booking.to_dict())
            booking._id = str(result.inserted_id)
            return booking.to_dict()
        except Exception as e:
            logging.error("Error creating booking: %s", e)
            raise

    @staticmethod
    def get_booking(booking_id):
        try:
            booking_data = current_app.mongo.db.bookings.find_one({"_id": ObjectId(booking_id)})
            if booking_data:
                booking = Booking.from_dict(booking_data)
                return booking.to_dict()
            return None
        except Exception as e:
            logging.error("Error getting booking: %s", e)
            raise

    @staticmethod
    def update_booking(booking_id, tripId=None, userId=None, seatNumber=None, status=None, updatedAt=None):
        try:
            update_fields = {}
            if tripId:
                update_fields["tripId"] = tripId
            if userId:
                update_fields["userId"] = userId
            if seatNumber:
                update_fields["seatNumber"] = seatNumber
            if status:
                update_fields["status"] = status
            if updatedAt:
                update_fields["updatedAt"] = updatedAt
            result = current_app.mongo.db.bookings.update_one(
                {"_id": ObjectId(booking_id)}, {"$set": update_fields}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error("Error updating booking: %s", e)
            raise

    @staticmethod
    def delete_booking(booking_id):
        try:
            result = current_app.mongo.db.bookings.delete_one({"_id": ObjectId(booking_id)})
            return result.deleted_count > 0
        except Exception as e:
            logging.error("Error deleting booking: %s", e)
            raise

    @staticmethod
    def get_all_bookings(page, size):
        try:
            skip = (page - 1) * size
            bookings_cursor = current_app.mongo.db.bookings.find().skip(skip).limit(size)
            bookings = [Booking.from_dict(booking).to_dict() for booking in bookings_cursor]
            total_bookings = current_app.mongo.db.bookings.count_documents({})
            return {
                "bookings": bookings,
                "pageSize": size,
                "currentPage": page,
                "totalData": total_bookings
            }
        except Exception as e:
            logging.error("Error getting all bookings: %s", e)
            raise

    @staticmethod
    def get_available_seats(tripId):
        try:
            booked_seats = current_app.mongo.db.bookings.find({"tripId": tripId, "status": "booked"})
            booked_seat_numbers = [booking["seatNumber"] for booking in booked_seats]
            return booked_seat_numbers
        except Exception as e:
            logging.error("Error getting available seats: %s", e)
            raise