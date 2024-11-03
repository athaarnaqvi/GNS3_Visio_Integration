import xml.etree.ElementTree as ET
import json
import sys
import os

# Define the namespace dictionary
NAMESPACES = {'visio': 'http://schemas.microsoft.com/office/visio/2012/main'}

def parse_pages_xml(pages_xml):
    """
    Parse pages1.xml to extract shapes and connections.
    
    :param pages_xml: Path to the pages1.xml file.
    :return: Dictionary of shapes and list of connection elements.
    """
    tree = ET.parse(pages_xml)
    root = tree.getroot()

    shapes = {}
    connections = []

    # Extract all shapes (devices) from pages1.xml
    for shape in root.findall(".//visio:Shape", NAMESPACES):
        shape_id = shape.get("ID")
        shape_name = shape.get("Name")
        master_id = shape.get("Master")
        if shape_id and master_id:
            shapes[shape_id] = {"name": shape_name, "master_id": master_id}

    # Extract all connections
    for connect in root.findall(".//visio:Connect", NAMESPACES):
        from_sheet = connect.get("FromSheet")
        to_sheet = connect.get("ToSheet")
        from_cell = connect.get("FromCell")
        connections.append({
            "from_sheet": from_sheet,
            "to_sheet": to_sheet,
            "from_cell": from_cell
        })

    return shapes, connections

def parse_masters_xml(masters_xml):
    """
    Parse masters.xml to map Master IDs to device names.
    
    :param masters_xml: Path to the masters.xml file.
    :return: Dictionary mapping master IDs to device names.
    """
    tree = ET.parse(masters_xml)
    root = tree.getroot()

    masters = {}
    for master in root.findall(".//visio:Master", NAMESPACES):
        master_id = master.get("ID")
        master_name = master.get("Name")
        if master_id:
            masters[master_id] = master_name

    return masters

def main(pages_xml, masters_xml, output_json):
    """
    Main function to parse pages1.xml and masters.xml, and output connections to a JSON file.
    
    :param pages_xml: Path to the pages1.xml file.
    :param masters_xml: Path to the masters.xml file.
    :param output_json: Path to the output JSON file.
    """
    # Parse the XML files
    shapes, connections = parse_pages_xml(pages_xml)
    masters = parse_masters_xml(masters_xml)

    processed_connections = []

    # Process each connection pair
    for i in range(0, len(connections), 2):
        conn1 = connections[i]
        if i + 1 < len(connections):
            conn2 = connections[i + 1]

            # Ensure both elements have the same FromSheet value
            if conn1['from_sheet'] == conn2['from_sheet']:
                # Determine the start and end based on FromCell
                if "BeginX" in conn1['from_cell']:
                    start_sheet = conn1['to_sheet']
                    end_sheet = conn2['to_sheet']
                else:
                    start_sheet = conn2['to_sheet']
                    end_sheet = conn1['to_sheet']

                # Get shape details
                start_shape = shapes.get(start_sheet)
                end_shape = shapes.get(end_sheet)

                if start_shape and end_shape:
                    # Map master IDs to names using masters.xml
                    start_name = masters.get(start_shape["master_id"], "Unknown Device")
                    end_name = masters.get(end_shape["master_id"], "Unknown Device")

                    # Append the shape IDs to the names without brackets
                    start_with_id = f"{start_name} {start_sheet}"
                    end_with_id = f"{end_name} {end_sheet}"

                    start_with_id = start_with_id.replace(' ','')
                    end_with_id = end_with_id.replace(' ','')

                    # Create a connection dictionary
                    connection = {
                        "from": start_with_id,
                        "to": end_with_id
                    }
                    
                    if connection not in processed_connections:  # Avoid duplicates
                        processed_connections.append(connection)

    # Write the processed connections to a JSON file
    with open(output_json, 'w') as json_file:
        json.dump(processed_connections, json_file, indent=4)

    print(f"Connections with appended IDs have been written to {output_json}")

if __name__ == "__main__":
    # Replace with actual file paths
    pages_xml = os.path.expanduser("~/Documents/VSCodeProjects/extracted_vsdx/visio/pages/page1.xml")
    masters_xml = os.path.expanduser("~/Documents/VSCodeProjects/extracted_vsdx/visio/masters/masters.xml")
    output_json = os.path.expanduser("~/Documents/VSCodeProjects/connections.json")
    
    main(pages_xml, masters_xml, output_json)
