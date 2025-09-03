import requests
from constant import get_constant


TTL_URL = get_constant("TTL_URL")

class TTLUtils:

    @staticmethod
    def get_ttl(id):
        try:
            ttl = requests.get(f"{TTL_URL}/{id}.ttl")
            return ttl.text
        except Exception as e:
            print(" TTL not Found!!!", e)
            return None
