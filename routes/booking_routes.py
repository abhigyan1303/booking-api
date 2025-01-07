# routes/booking_routes.py
from flask import Blueprint, request, jsonify
from facade.booking_facade import BookingFacade
from decorators import token_required, permission_required

booking_bp = Blueprint('booking_bp', __name__)

@booking_bp.route('/booking/create', methods=['POST'])
@token_required
@permission_required('user')
def create_booking(current_user, current_user_role):
    """
    Creates a new booking for a given trip and user.

    Args:
        data (dict): Request body data with the following keys:
            - tripId (str): The ID of the trip to book.
            - seatNumber (int): The seat number to book.
            - status (str): The status of the booking (will be overwritten to 'booked').

    Returns:
        dict: The newly created booking as a JSON object.
    """
    data = request.get_json()
    booking = BookingFacade.create_booking(
        tripId=data['tripId'],
        userId=current_user,
        seatNumber=data['seatNumber'],
        status='booked'
    )
    return jsonify(booking)

@booking_bp.route('/booking/<booking_id>', methods=['GET'])
@token_required
@permission_required('user')
def get_booking(booking_id, current_user, current_user_role):
    """
    Retrieves a booking by its ID.

    Args:
        booking_id (str): The ID of the booking to retrieve.

    Returns:
        dict: The booking as a JSON object if found, otherwise a JSON error
            message with a 404 status code.
    """
    booking = BookingFacade.get_booking(booking_id)
    if booking:
        return jsonify(booking)
    return jsonify({'error': 'Booking not found'}), 404

@booking_bp.route('/booking/<booking_id>', methods=['PUT'])
@token_required
@permission_required('user')
def update_booking(booking_id, current_user, current_user_role):
    """
    Updates an existing booking's details.

    Args:
        booking_id (str): The ID of the booking to update.
        data (dict): Request body data with the following keys:
            - tripId (str): The ID of the trip the booking belongs to.
            - userId (str): The ID of the user who made the booking.
            - seatNumber (int): The seat number of the booking.
            - status (str): The status of the booking (will be overwritten to 'booked').
            - updatedAt (datetime): The time when the booking was updated.

    Returns:
        dict: A JSON object with a success message if the update was successful, otherwise a JSON error
            message with a 404 status code.
    """
    data = request.get_json()
    success = BookingFacade.update_booking(
        booking_id,
        tripId=data.get('tripId'),
        userId=current_user,
        seatNumber=data.get('seatNumber'),
        status=data.get('status'),
        updatedAt=data.get('updatedAt')
    )
    if success:
        return jsonify({'message': 'Booking updated'})
    return jsonify({'error': 'Booking not found'}), 404

@booking_bp.route('/booking/<booking_id>', methods=['DELETE'])
@token_required
@permission_required('user')
def delete_booking(booking_id, current_user, current_user_role):
    """
    Deletes a booking.

    Args:
        booking_id (str): The ID of the booking to delete.

    Returns:
        dict: A JSON object with a success message if the booking was successfully deleted, otherwise a JSON error
            message with a 404 status code.
    """
    success = BookingFacade.delete_booking(booking_id)
    if success:
        return jsonify({'message': 'Booking deleted'})
    return jsonify({'error': 'Booking not found'}), 404

@booking_bp.route('/booking/list', methods=['GET'])
@token_required
@permission_required('admin')
def list_bookings(current_user, current_user_role):
    """
    Lists all bookings.

    :param page: The page to retrieve (default is 1).
    :param size: The size of the page (default is 10).

    :return: A JSON object containing the list of bookings.
    :statuscode 200: The list of bookings was successfully retrieved.
    """
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    bookings_data = BookingFacade.get_all_bookings(page, size)
    return jsonify(bookings_data)

@booking_bp.route('/booking/available_seats/<trip_id>', methods=['GET'])
@token_required
@permission_required('user')
def available_seats(trip_id, current_user, current_user_role):
    """
    Retrieves the booked seat numbers for a given trip.

    Args:
        trip_id (str): The ID of the trip to retrieve the booked seats for.

    Returns:
        dict: A JSON object containing a list of booked seat numbers.
    """
    booked_seats = BookingFacade.get_available_seats(trip_id)
    return jsonify({"booked_seats": booked_seats})