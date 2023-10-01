from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)

# Declare a method to handle @app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def close_storage(exception):
    storage.close()

if __name__ == "__main__":
    # Get the host and port from environment variables or use defaults
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    
    # Run your Flask server (variable app) with the specified host, port, and threaded=True
    app.run(host=host, port=port, threaded=True)
