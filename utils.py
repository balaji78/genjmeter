#
# GenJmeter - Utility Functions
# Developer: BalajiVenkateswaran K
# Version: 1.0
#

from urllib.parse import urlparse
import html

def html_encode_json_body(json_body):
    # Convert special characters to HTML entities
    encoded_json_body = html.escape(json_body)
    return encoded_json_body

def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def get_protocol(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme

def get_path(url):
    parsed_url = urlparse(url)
    return parsed_url.path

def get_port(url):
    parsed_url = urlparse(url)
    return parsed_url.port or ('443' if get_protocol(url) == 'https' else '80')

def url_contains(url, keywords):
    for keyword in keywords:
        if keyword in url:
            return True
    return False

def method_contains(method, keywords):
    for keyword in keywords:
        if keyword in method:
            return True
    return False

def trim_path(input_string):
    index = input_string.rfind('/')  # Find the index of the last occurrence of '/'
    if index != -1:
        substring = input_string[index + 1:]  # Extract the substring from index + 1 to the end
    else:
        substring = input_string  # If '/' is not found, return the original string    
    return substring