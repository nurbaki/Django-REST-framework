from .base import * 
 
env_name = config("ENV_NAME") 
 
if env_name == "prod": 
    # production settings:
    from .prod import * 
elif env_name == "dev": 
    # development settings:
    from .dev import * 