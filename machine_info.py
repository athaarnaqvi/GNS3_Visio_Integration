# import xml.etree.ElementTree as ET
# import os

# def parse_xml(file_path):
#     # Parse the XML file and return the root element
#     tree = ET.parse(file_path)
#     return tree.getroot()

# def extract_machine_names(page_root):
#     # Extract names of machines from the page XML
#     machine_names = []
#     master_name_map = {}
#     master_id_map={}
#     # Traverse the XML to find all 'Shape' elements
#     for shape in page_root.findall('.//Shape', namespaces={'': "http://schemas.microsoft.com/office/visio/2012/main"}):
#         shape_id = shape.get('ID')  # Get the unique 'ID' attribute for each shape
#         name = shape.get('NameU')  # Get the 'NameU' attribute for machine names
#         master = shape.get('Master')  # Get the 'Master' ID if present
        

#         if name:
#             namex = name+shape_id
#             machine_names.append(f"{namex}")
#             if master:
               
#                 # Map MasterID to NameU for future shapes with the same master
                
#                 master_name_map[master] = name
                
                
#         elif master and master in master_name_map:
#             # If NameU is not available but master is, use the mapped name
#             namey = master_name_map[master]+shape_id
#             machine_names.append(f"{namey}")
       

#     return machine_names

# def save_to_file(data, output_file):
#     # Save the extracted names to a plain text file
#     with open(output_file, 'w') as f:
#         for name in data:
#             f.write(name + '\n')
#     print(f"Machine names have been saved to {output_file}")

# def main():
#     # Path to the specific page XML file
    
#     page_file=os.path.expanduser("~/Documents/VSCodeProjects/extracted_vsdx/visio/pages/page1.xml")
#     # Parse the page XML
#     page_root = parse_xml(page_file)

#     # Extract machine names from the page
#     machine_names = extract_machine_names(page_root)
#     for m in machine_names:
#         if 'Rack Frame' in m or 'Dynamic connector' in m:
#             machine_names.remove(m)
#     for i in range(len(machine_names)):
#         machine_names[i] = machine_names[i].replace(' ', '')
#     # Output file path for the extracted machine names
#     output_file = os.path.expanduser("~/Documents/VSCodeProjects/machine_names.txt")
#     # Save the extracted machine names to the output file
#     save_to_file(machine_names, output_file)

# if __name__ == "__main__":
#     main()

import xml.etree.ElementTree as ET
import os

def parse_xml(file_path):
    # Parse the XML file and return the root element
    tree = ET.parse(file_path)
    return tree.getroot()

def extract_machine_names(page_root):
    # Extract names of machines from the page XML
    machine_names = []
    master_name_map = {}
    
    # Traverse the XML to find all 'Shape' elements
    for shape in page_root.findall('.//Shape', namespaces={'': "http://schemas.microsoft.com/office/visio/2012/main"}):
        shape_id = shape.get('ID')  # Get the unique 'ID' attribute for each shape
        name = shape.get('NameU')  # Get the 'NameU' attribute for machine names
        master = shape.get('Master')  # Get the 'Master' ID if present
        
        # Filter out unwanted shapes based on NameU
        if name and ('Rack Frame' not in name and 'Dynamic connector' not in name):
            namex = name + shape_id
            machine_names.append(namex)
            if master:
                # Map MasterID to NameU for future shapes with the same master
                master_name_map[master] = name
        elif master and master in master_name_map:
            # If NameU is not available but master is, use the mapped name
            namey = master_name_map[master] + shape_id
            machine_names.append(namey)

    return machine_names

def save_to_file(data, output_file):
    # Save the extracted names to a plain text file
    with open(output_file, 'w') as f:
        for name in data:
            f.write(name + '\n')
    print(f"Machine names have been saved to {output_file}")

def main():
    # Path to the specific page XML file
    page_file = os.path.expanduser("~/Documents/VSCodeProjects/extracted_vsdx/visio/pages/page1.xml")
    
    # Parse the page XML
    page_root = parse_xml(page_file)

    # Extract machine names from the page
    machine_names = extract_machine_names(page_root)
    
    # Remove spaces from machine names
    machine_names = [name.replace(' ', '') for name in machine_names]

    # Output file path for the extracted machine names
    output_file = os.path.expanduser("~/Documents/VSCodeProjects/machine_names.txt")
    
    # Save the extracted machine names to the output file
    save_to_file(machine_names, output_file)

if __name__ == "__main__":
    main()
