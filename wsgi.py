import os
from apps.app import create_app
from waitress import serve
from dotenv import load_dotenv

load_dotenv()

config_key = os.getenv("FLASK_CONFIG", "dev")
app = create_app(config_key)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
    
    
    
    
    
    
    
    
    
    
    
    
    
    