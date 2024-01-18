from xml.dom import minidom
import json
from bs4 import BeautifulSoup

def format_xml(input_string):
    """Formats string to XML

    Args:
        input_string (str): input string

    Returns:
        str: formatted XML string
    """
    # parse the XML string and return formatted XML string
    xml_dom = minidom.parseString(input_string)
    formatted_xml = xml_dom.toprettyxml()
    return formatted_xml

def format_json(input_string):
    """Formats string to JSON

    Args:
        input_string (str): input string

    Returns:
        str: formatted JSON string
    """
    # parse the JSON string and return formatted JSON string
    formatted_json = json.dumps(input_string, indent=2, sort_keys=True)
    return formatted_json


def format_html(input_string):
    """Formats string to HTML

    Args:
        input_string (str): input string

    Returns:
        str: formatted HTML string
    """
    # parse the HTML string and return formatted HTML string
    formatted_html = BeautifulSoup(input_string, 'html.parser').prettify()
    return formatted_html

def prepare_headers(payload_type, headers_dict):
    """Prepares the request headers dict

    Args:
        payload_type (str): the payload type ['xml', 'json']
        headers_dict (dict): the list of key and values generated from the data editor 'hdrs_input' in the format of {'key':[''],'value':['']}

    Returns:
        dict: Request headers
    """
    headers = {}
    if payload_type:
        content_type = 'application/' + payload_type
        headers = {'Content-Type': content_type}
    for i in range(len(headers_dict['key'])):
        if headers_dict['key'][i]=='':
            continue
        else:
            headers.update({headers_dict['key'][i]:headers_dict['value'][i]})
    return headers