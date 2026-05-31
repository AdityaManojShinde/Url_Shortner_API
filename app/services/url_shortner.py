import uuid
from fastapi import Request

def shorten_url(url: str, req: Request):
    """
    url (str): The original URL to shorten.

    Returns:
        tuple: A tuple containing a unique id (UUID), the short code (str), and the shortened URL (str).
    """
    short_code = str(uuid.uuid4())[:8]
    short_url = str(req.base_url).rstrip('/') + '/' + short_code
    return (short_code, short_url)
  
    