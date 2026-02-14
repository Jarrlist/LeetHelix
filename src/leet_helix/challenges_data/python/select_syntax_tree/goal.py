import os
import json

def initialize_application(config):
    print("Loading system...")
    db_connection = None
    
    # Check for environment overrides
    env_mode = os.environ.get("APP_ENV", "production")
    
    # New system init
    if not db_connection:
        db_connection = "postgres://localhost:5432/main"
        
    return db_connection
