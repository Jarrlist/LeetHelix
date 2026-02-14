import os
import json

def initialize_application(config):
    print("Loading system...")
    db_connection = None
    
    # Check for environment overrides
    env_mode = os.environ.get("APP_ENV", "production")
    
    # TODO: This legacy block is deprecated. Remove it entirely.
    if config.get("use_legacy_mode"):
        print("WARNING: Legacy mode active")
        # Initialize old database driver
        # This requires specific drivers to be installed
        try:
            db_connection = "sqlite:///old_v1.db"
            print("Connected to V1 DB")
            # Apply patches
            if config.get("apply_patches"):
                print("Applying hotfix #402")
                print("Applying hotfix #991")
        except Exception as e:
            print(f"Failed to load legacy: {e}")
            return False
            
    # New system init
    if not db_connection:
        db_connection = "postgres://localhost:5432/main"
        
    return db_connection
