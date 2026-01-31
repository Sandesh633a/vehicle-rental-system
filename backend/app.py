from flask import Flask, jsonify

# 1️⃣ App configuration (env variables, secrets)
from config import Config

# 2️⃣ Extensions (JWT + MongoDB init)
from extensions import jwt, init_db

# 3️⃣ Blueprints (routes)
from routes.auth import auth_bp
from routes.admin import admin_bp

from routes.dealership import dealership_bp
from routes.vehicle import vehicle_bp


from routes.booking import booking_bp



def create_app():
    """
    Application Factory:
    Creates and configures the Flask app.
    This pattern is industry-standard and scalable.
    """
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object(Config)

    # Initialize JWT (authentication system)
    jwt.init_app(app)

    # Initialize MongoDB connection
    # This sets extensions.db once and shares it across the app
    init_db(app.config["MONGO_URI"])

    # Register route blueprints
    app.register_blueprint(auth_bp)     # /auth/*
    app.register_blueprint(admin_bp)    # /admin/*



    app.register_blueprint(dealership_bp)
    app.register_blueprint(vehicle_bp)

    app.register_blueprint(booking_bp)



    # Health check endpoint (used for testing & deployment)
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "OK"}), 200

    return app


# Create app instance
app = create_app()

# Run in development mode
if __name__ == "__main__":
    app.run()