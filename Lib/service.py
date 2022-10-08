# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from config import DEFAULT_SERVICE
from Music  import available_services

def get_default_service() -> str:
    services = list(available_services.keys())

    try:
        config_service = DEFAULT_SERVICE.lower()
    
        if config_service in services:
            return config_service
        else:          # Invalid DEFAULT_SERVICE
            return "youtube"
    except NameError:  # DEFAULT_SERVICE not defined
        return "youtube"