import xml.etree.ElementTree as ET
from typing import Generator, Dict


def parse_xml(file_path: str) -> Generator[Dict[str, str], None, None]:
    """
    Parses XML file and return the rows as Generator
    """

    # parse the xml file
    tree = ET.parse(file_path)

    # get the root
    root = tree.getroot()

    for tu_element in root.findall('.//tu'):
        tu_dict = {}
        for tuv_element in tu_element.findall('./tuv'):
            lang = tuv_element.get('{http://www.w3.org/XML/1998/namespace}lang')
            text = tuv_element.find('./seg').text
            tu_dict[lang] = text
        yield tu_dict
