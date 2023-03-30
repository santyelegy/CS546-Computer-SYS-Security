import sys
from urllib.parse import urlparse

def http_program(url: str) -> bool:
    supported_schemes = ["http", "https"]
    result = urlparse(url)
    if result.scheme not in supported_schemes:
        raise ValueError("Scheme must be one of " + 
                         repr(supported_schemes))
    if result.netloc == '':
        raise ValueError("Host must be non-empty")
    # Do something with the URL
    return True


if __name__ == '__main__':
    for line in sys.stdin:
        http_program(line)