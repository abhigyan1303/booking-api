# routes/bus_route_routes.py
from flask import Blueprint, request, jsonify
from facade.bus_route_facade import BusRouteFacade
from decorators import token_required, permission_required

bus_route_bp = Blueprint('bus_route_bp', __name__)

@bus_route_bp.route('/bus_route/create', methods=['POST'])
@token_required
@permission_required('admin')
def create_route(current_user, current_user_role):
    """
    Creates a new bus route.

    Args:
        route (str): The route description.
        routeNo (str): The route number.
        distance (float): The distance of the route.
        createdBy (User): The user who created the route.

    Returns:
        dict: The newly created bus route as a JSON object.
    """
    data = request.get_json()
    bus_route = BusRouteFacade.create_route(
        route=data['route'],
        routeNo=data['routeNo'],
        distance=data['distance'],
        createdBy=current_user
    )
    return jsonify(bus_route)

@bus_route_bp.route('/bus_route/<route_id>', methods=['GET'])
@token_required
@permission_required('user')
def get_route(route_id, current_user, current_user_role):
    """
    Gets a bus route by its ID.

    Args:
        route_id (str): The ID of the bus route.

    Returns:
        dict: The bus route as a JSON object, or an error message if the route is not found.
    """

    bus_route = BusRouteFacade.get_route(route_id)
    if bus_route:
        return jsonify(bus_route)
    return jsonify({'error': 'Bus route not found'}), 404

@bus_route_bp.route('/bus_route/<route_id>', methods=['PUT'])
@token_required
@permission_required('admin')
def update_route(route_id, current_user, current_user_role):
    """
    Updates a bus route by its ID.

    Args:
        route_id (str): The ID of the bus route.

    Request Body:
        route (str): The route description.
        routeNo (str): The route number.
        distance (float): The distance of the route.

    Returns:
        dict: A JSON object with a message saying the route was updated, or an error message if the route is not found.
    """
    data = request.get_json()
    success = BusRouteFacade.update_route(
        route_id,
        route=data.get('route'),
        routeNo=data.get('routeNo'),
        distance=data.get('distance'),
        updatedAt=data.get('updatedAt')
    )
    if success:
        return jsonify({'message': 'Bus route updated'})
    return jsonify({'error': 'Bus route not found'}), 404

@bus_route_bp.route('/bus_route/<route_id>', methods=['DELETE'])
@token_required
@permission_required('admin')
def delete_route(route_id, current_user, current_user_role):
    """
    Deletes a bus route by its ID.

    :param route_id: The ID of the bus route to be deleted.
    :return: A success message if the bus route was successfully deleted, otherwise an error message.
    :statuscode 200: The bus route was successfully deleted.
    :statuscode 404: The bus route was not found.
    """
    success = BusRouteFacade.delete_route(route_id)
    if success:
        return jsonify({'message': 'Bus route deleted'})
    return jsonify({'error': 'Bus route not found'}), 404

@bus_route_bp.route('/bus_route/list', methods=['GET'])
@token_required
@permission_required('user')
def list_routes(current_user, current_user_role):
    """
    Lists all bus routes.

    Args:
        page (int): The page number. Defaults to 1.
        size (int): The page size. Defaults to 10.

    Returns:
        dict: A JSON object containing the list of bus routes.
    """
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    routes_data = BusRouteFacade.get_all_routes(page, size)
    return jsonify(routes_data)
# ...existing code...

@bus_route_bp.route('/city/add', methods=['POST'])
@token_required
@permission_required('admin')
def add_city(current_user, current_user_role):
    """
    Adds a new city.

    Args:
        name (str): The name of the city.

    Returns:
        dict: The newly added city as a JSON object.
    """
    data = request.get_json()
    city = BusRouteFacade.add_city(data['name'])
    return jsonify(city)

@bus_route_bp.route('/cities', methods=['GET'])
@token_required
def list_cities(current_user, current_user_role):
    """
    Lists cities based on a query.

    Args:
        query (str): The query string to search for cities.

    Returns:
        list: A JSON array of cities matching the query.
    """
    query = request.args.get('query', '')
    cities = BusRouteFacade.list_cities(query)
    return jsonify(cities)