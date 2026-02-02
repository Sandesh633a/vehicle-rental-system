# from flask import Flask, jsonify

# # 1️⃣ App configuration (env variables, secrets)
# from config import Config

# # 2️⃣ Extensions (JWT + MongoDB init)
# from extensions import jwt, init_db

# # 3️⃣ Blueprints (routes)
# from routes.auth import auth_bp
# from routes.admin import admin_bp

# from routes.dealership import dealership_bp
# from routes.vehicle import vehicle_bp


# from routes.booking import booking_bp



# def create_app():
#     """
#     Application Factory:
#     Creates and configures the Flask app.
#     This pattern is industry-standard and scalable.
#     """
#     app = Flask(__name__)

#     # Load configuration from config.py
#     app.config.from_object(Config)

#     # Initialize JWT (authentication system)
#     jwt.init_app(app)

#     # Initialize MongoDB connection
#     # This sets extensions.db once and shares it across the app
#     init_db(app.config["MONGO_URI"])

#     # Register route blueprints
#     app.register_blueprint(auth_bp)     # /auth/*
#     app.register_blueprint(admin_bp)    # /admin/*



#     app.register_blueprint(dealership_bp)
#     app.register_blueprint(vehicle_bp)

#     app.register_blueprint(booking_bp)



#     # Health check endpoint (used for testing & deployment)
#     @app.route("/health", methods=["GET"])
#     def health():
#         return jsonify({"status": "OK"}), 200

#     return app


# # Create app instance
# app = create_app()

# # Run in development mode
# if __name__ == "__main__":
#     app.run()


















from flask import Flask, jsonify
from flask_cors import CORS

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

    # 🔥 ENABLE CORS (CRITICAL FOR FRONTEND)
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Load configuration from config.py
    app.config.from_object(Config)

    # Initialize JWT (authentication system)
    jwt.init_app(app)

    # Initialize MongoDB connection
    # This sets extensions.db once and shares it across the app
    init_db(app.config["MONGO_URI"])

    # Register route blueprints
    app.register_blueprint(auth_bp)       # /auth/*
    app.register_blueprint(admin_bp)      # /admin/*
    app.register_blueprint(dealership_bp) # /dealership/*
    app.register_blueprint(vehicle_bp)    # /vehicles/*
    app.register_blueprint(booking_bp)    # /bookings/*

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "OK"}), 200

    return app


# Create app instance (used by Gunicorn / Render)
app = create_app()

# Run in development mode (local only)
if __name__ == "__main__":
    app.run(debug=True)