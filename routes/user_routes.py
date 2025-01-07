from flask import Blueprint, request, jsonify, current_app
from facade.user_facade import UserFacade
from decorators import token_required, permission_required

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def hello_user():
    """
    Says hello and returns the version of the API.

    :return: A JSON object with the API version.
    :statuscode 200: The API version was returned.
    """
    return jsonify({'version': current_app.config['VERSION']}), 200

@user_bp.route('/user/create', methods=['POST'])
def create_user():
    """
    Creates a new user.

    :param firstName: The user's first name.
    :param lastName: The user's last name.
    :param email: The user's email address.
    :param username: The user's username.
    :param password: The user's password.
    :param mobile: The user's mobile number (optional).
    :param gender: The user's gender (optional).

    :return: The newly created user as a JSON object.
    """
    data = request.get_json()
    user = UserFacade.create_user(
        data['firstName'],
        data['lastName'],
        data['email'],
        data['username'],
        data['password'],
        data.get('mobile'),
        data.get('gender')
    )
    return jsonify(user)

@user_bp.route('/user/login', methods=['POST'])
def login():
    """
    Logs a user in.

    :param username: The user's username.
    :param password: The user's password.

    :return: The JWT token as a JSON object.
    :statuscode 200: The user was successfully logged in.
    :statuscode 401: The user credentials are invalid.
    """
    data = request.get_json()
    token = UserFacade.login(data['username'], data['password'])
    if token:
        return jsonify(token)
    return jsonify({'error': 'Invalid credentials'}), 401

@user_bp.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user(user_id, current_user, current_user_role):
    """
    Gets a user by its ID.

    :param user_id: The ID of the user to be retrieved.

    :return: The user as a JSON object.
    :statuscode 200: The user was found.
    :statuscode 404: The user was not found.
    """
    user = UserFacade.get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/user/<user_id>', methods=['PUT'])
@token_required
@permission_required('admin')
def update_user(user_id, current_user, current_user_role):
    """
    Updates an existing user's information.

    :param user_id: The ID of the user to be updated.
    :return: A success message if the update was successful, otherwise an error message.
    :statuscode 200: The user was successfully updated.
    :statuscode 404: The user was not found.
    """
    user = UserFacade.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    success = UserFacade.update_user(
        user_id,
        data.get('firstName', user.get('firstName')),
        data.get('lastName', user.get('lastName')),
        data.get('email', user.get('email')),
        data.get('username', user.get('username')),
        data.get('password', user.get('password')),
        data.get('mobile', user.get('mobile')),
        data.get('gender', user.get('gender')),
        data.get('userType', user.get('userType')),
        data.get('userGroup', user.get('userGroup'))
    )
    if success:
        return jsonify({'message': 'User updated'})
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/user/<user_id>', methods=['DELETE'])
@token_required
@permission_required('admin')
def delete_user(user_id, current_user, current_user_role):
    """
    Deletes a user.

    :param user_id: The ID of the user to be deleted.
    :return: A success message if the user was successfully deleted, otherwise an error message.
    :statuscode 200: The user was successfully deleted.
    :statuscode 404: The user was not found.
    """
    success = UserFacade.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted'})
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/user/list', methods=['GET'])
@token_required
@permission_required('superAdmin')
def list_users(current_user, current_user_role):
    """
    Lists all users.

    :param page: The page to retrieve (default is 1).
    :param size: The size of the page (default is 10).

    :return: A JSON object containing the list of users.
    :statuscode 200: The list of users was successfully retrieved.
    """
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    users_data = UserFacade.get_users(page, size)
    return jsonify(users_data)