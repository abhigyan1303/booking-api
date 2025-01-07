import os

from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

from routes.booking_routes import booking_bp
from routes.bus_route_routes import bus_route_bp
from routes.bus_routes import bus_bp
from routes.bus_trip_routes import bus_trip_bp
from routes.user_routes import user_bp

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
ver = os.getenv("VERSION", "v1")
app.config["VERSION"] = ver

mongo = PyMongo(app)
app.mongo = mongo

# Enable CORS for all routes
CORS(app)

base_url = f"/{ver}/api"
app.register_blueprint(user_bp, url_prefix=base_url)
app.register_blueprint(bus_bp, url_prefix=base_url)
app.register_blueprint(bus_route_bp, url_prefix=base_url)
app.register_blueprint(bus_trip_bp, url_prefix=base_url)
app.register_blueprint(booking_bp, url_prefix=base_url)

if __name__ == '__main__':
    app.run(debug=True)
