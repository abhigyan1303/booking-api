# This file contains routes for bus related operations. 
# The routes are protected by token_required decorator.
# The routes are as follows:
from flask import Blueprint, request, jsonify
from facade.bus_facade import BusFacade
from decorators import token_required, permission_required

bus_bp = Blueprint('bus_bp', __name__)

@bus_bp.route('/bus/create', methods=['POST'])
@token_required
@permission_required('admin')
def create_bus(current_user):
    """
    Creates a new bus.

    Args:
        travel (str): The travel agency that owns the bus.
        isAc (bool): Whether the bus is air-conditioned or not.
        isSleeper (bool): Whether the bus is a sleeper bus or not.
        registration (str): The registration number of the bus.
        totalSeat (int): The total number of seats in the bus.
        insuranceValidTill (datetime): The date until which the insurance of the bus is valid.
        permitValidTill (datetime): The date until which the permit of the bus is valid.
        createdBy (User): The user who created the bus.

    Returns:
        dict: The newly created bus as a JSON object.
    """
    data = request.get_json()
    bus = BusFacade.create_bus(
        travel=data['travel'],
        isAc=data['isAc'],
        isSleeper=data['isSleeper'],
        registration=data['registration'],
        totalSeat=data['totalSeat'],
        insuranceValidTill=data['insuranceValidTill'],
        permitValidTill=data['permitValidTill'],
        createdBy=current_user
    )
    return jsonify(bus)

@bus_bp.route('/bus/<bus_id>', methods=['GET'])
@token_required
@permission_required('user')
def get_bus(bus_id):
    """
    Retrieves a bus by its ID.

    Args:
        bus_id (str): The ID of the bus to retrieve.

    Returns:
        dict: A JSON object of the bus details if found, or an error message if not found.
    """

    bus = BusFacade.get_bus(bus_id)
    if bus:
        return jsonify(bus)
    return jsonify({'error': 'Bus not found'}), 404

@bus_bp.route('/bus/<bus_id>', methods=['PUT'])
@token_required
@permission_required('admin')
def update_bus(bus_id, current_user, current_user_role):
    """
    Updates an existing bus's details by its ID.

    Args:
        bus_id (str): The ID of the bus to update.

    Request Body:
        travel (str): The travel agency that owns the bus.
        isAc (bool): Whether the bus is air-conditioned or not.
        isSleeper (bool): Whether the bus is a sleeper bus or not.
        registration (str): The registration number of the bus.
        totalSeat (int): The total number of seats in the bus.
        insuranceValidTill (datetime): The date until which the insurance of the bus is valid.
        permitValidTill (datetime): The date until which the permit of the bus is valid.
        updatedAt (datetime): The time when the bus information was last updated.

    Returns:
        dict: A JSON object with a message indicating the bus was updated, or an error message if the bus is not found.
    """

    data = request.get_json()
    success = BusFacade.update_bus(
        bus_id,
        travel=data.get('travel'),
        isAc=data.get('isAc'),
        isSleeper=data.get('isSleeper'),
        registration=data.get('registration'),
        totalSeat=data.get('totalSeat'),
        insuranceValidTill=data.get('insuranceValidTill'),
        permitValidTill=data.get('permitValidTill'),
        updatedAt=data.get('updatedAt')
    )
    if success:
        return jsonify({'message': 'Bus updated'})
    return jsonify({'error': 'Bus not found'}), 404

@bus_bp.route('/bus/<bus_id>', methods=['DELETE'])
@token_required
@permission_required('admin')
def delete_bus(bus_id, current_user, current_user_role):
    """
    Deletes a bus by its ID.

    Args:
        bus_id (str): The ID of the bus to delete.

    Returns:
        dict: A JSON object with a message indicating the bus was deleted, or an error message if the bus is not found.
    """
    success = BusFacade.delete_bus(bus_id)
    if success:
        return jsonify({'message': 'Bus deleted'})
    return jsonify({'error': 'Bus not found'}), 404

@bus_bp.route('/bus/list', methods=['GET'])
@token_required
@permission_required('user')
def list_buses(current_user, current_user_role):
    """
    Lists all buses.

    Args:
        page (int): The page number (default is 1).
        size (int): The page size (default is 10).

    Returns:
        dict: A JSON object containing the list of buses.
    """
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    buses_data = BusFacade.get_all_buses(page, size)
    return jsonify(buses_data)