# routes/bus_trip_routes.py
from flask import Blueprint, request, jsonify
from facade.bus_trip_facade import BusTripFacade
from decorators import token_required, permission_required

bus_trip_bp = Blueprint('bus_trip_bp', __name__)

@bus_trip_bp.route('/bus_trip/create', methods=['POST'])
@token_required
@permission_required('admin')
def create_trip(current_user, current_user_role):
    """
    Creates a new bus trip.

    Args:
        routeId (str): The ID of the bus route for the trip.
        date (str): The date of the trip in the format %Y-%m-%d.
        frequency (str): The frequency of the trip (daily, weekly, monthly).
        timing (str): The timing of the trip (morning, afternoon, evening).
        fare (float): The fare of the trip.
        stops (list): A list of stops for the trip.
        createdBy (User): The user who created the trip.

    Returns:
        dict: The newly created bus trip as a JSON object.
    """
    data = request.get_json()
    bus_trip = BusTripFacade.create_trip(
        routeId=data['routeId'],
        date=data['date'],
        frequency=data['frequency'],
        timing=data['timing'],
        fare=data['fare'],
        stops=data['stops'],
        createdBy=current_user
    )
    return jsonify(bus_trip)

@bus_trip_bp.route('/bus_trip/<trip_id>', methods=['GET'])
@token_required
@permission_required('user')
def get_trip(trip_id, current_user, current_user_role):
    """
    Retrieves a bus trip by its ID.

    Args:
        trip_id (str): The ID of the bus trip to retrieve.

    Returns:
        dict: The bus trip as a JSON object, or an error message if the trip is not found.
    """
    bus_trip = BusTripFacade.get_trip(trip_id)
    if bus_trip:
        return jsonify(bus_trip)
    return jsonify({'error': 'Bus trip not found'}), 404

@bus_trip_bp.route('/bus_trip/<trip_id>', methods=['PUT'])
@token_required
@permission_required('admin')
def update_trip(trip_id, current_user, current_user_role):
    """
    Updates an existing bus trip's details by its ID.

    Args:
        trip_id (str): The ID of the bus trip to update.

    Request Body:
        routeId (str): The ID of the new bus route for the trip.
        date (str): The new date of the trip in the format %Y-%m-%d.
        frequency (str): The new frequency of the trip (daily, weekly, monthly).
        timing (str): The new timing of the trip (morning, afternoon, evening).
        fare (float): The new fare of the trip.
        stops (list): The new list of stops for the trip.
        updatedAt (datetime): The time when the trip was updated.

    Returns:
        dict: A JSON object with a success message if the update was successful, otherwise a JSON error message with a 404 status code.
    """

    data = request.get_json()
    success = BusTripFacade.update_trip(
        trip_id,
        routeId=data.get('routeId'),
        date=data.get('date'),
        frequency=data.get('frequency'),
        timing=data.get('timing'),
        fare=data.get('fare'),
        stops=data.get('stops'),
        updatedAt=data.get('updatedAt')
    )
    if success:
        return jsonify({'message': 'Bus trip updated'})
    return jsonify({'error': 'Bus trip not found'}), 404

@bus_trip_bp.route('/bus_trip/<trip_id>', methods=['DELETE'])
@token_required
@permission_required('admin')
def delete_trip(trip_id, current_user, current_user_role):
    """
    Deletes a bus trip by its ID.

    Args:
        trip_id (str): The ID of the bus trip to delete.

    Returns:
        dict: A JSON object with a success message if the bus trip was successfully deleted, otherwise a JSON error message with a 404 status code.
    """
    success = BusTripFacade.delete_trip(trip_id)
    if success:
        return jsonify({'message': 'Bus trip deleted'})
    return jsonify({'error': 'Bus trip not found'}), 404

@bus_trip_bp.route('/bus_trip/list', methods=['GET'])
@token_required
@permission_required('user')
def list_trips(current_user, current_user_role):
    """
    Lists all bus trips.

    Args:
        page (int): The page number to retrieve (default is 1).
        size (int): The page size (default is 10).

    Returns:
        dict: A JSON object containing the list of bus trips.
    """
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    date = request.args.get('date')
    busTypes = request.args.get('busTypes')
    from_city = request.args.get('from')
    to_city = request.args.get('to')
    trips_data = BusTripFacade.get_all_trips(page, size, date, busTypes, from_city, to_city)
    return jsonify(trips_data)