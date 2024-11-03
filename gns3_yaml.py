import os

def read_vsdx_path():
    """Read the saved VSDX file path from the 'vsdx_path' file."""
    with open("vsdx_path.txt", "r") as file:
        vsdx_file_path = file.read().strip()
    return vsdx_file_path

def get_project_name_from_vsdx(vsdx_path):
    """Extract the project name from the VSDX file name without the extension."""
    return os.path.splitext(os.path.basename(vsdx_path))[0]

def read_machine_info(file_path):
    """Read the machine names from the machine_info.txt file."""
    machine_info = []
    with open(file_path, 'r') as file:
        for line in file:
            machine_info.append(line.strip())
    return machine_info

def generate_yaml(machine_info, output_file, project_name):
    """Generate the YAML file based on the machine info."""
    yaml_content = f"""\
- hosts: localhost
  gather_facts: no
  vars:
    gns3_url: "http://127.0.0.1:3080"  # Replace with your GNS3 server URL
    ansible_python_interpreter: /usr/bin/python3
    compute_id: "local"  # Ensure this matches your compute ID
  tasks:
    - name: Create a new GNS3 project
      uri:
        url: "{{{{ gns3_url }}}}/v2/projects"
        method: POST
        headers:
          Content-Type: "application/json"
        body: |
          {{
            "name": "{project_name}"
          }}
        body_format: json
        return_content: yes
        status_code: 201
      register: project_result

    - name: Debug project creation result
      debug:
        var: project_result
"""
    
    # Coordinates for device placement on the canvas
    x_coord = 0
    y_coord = 100
    x_step = 15  # Increment x-coordinate for next device placement
    
    switchcount = 0
    routercount = 0
    # Loop through each machine info and add corresponding device
    for i, machine in enumerate(machine_info, start=1):
        node_type = ""
        template_id = ""
       
        # Determine the node type and template ID based on the machine type        
        node_type = "ethernet_switch"        
        template_id = "39e257dc-8412-3174-b6b3-0ee3ed6a43e9"  # Replace with the actual template ID for switches
        symbol =  ":/symbols/ethernet_switch.svg"
        switchcount+=1
        device_name = f"{machine}"
        yaml_content += f"""
    - name: Add {device_name} to the project
      uri:
        url: "{{{{ gns3_url }}}}/v2/projects/{{{{ project_result.json.project_id }}}}/nodes"
        method: POST
        headers:
          Content-Type: "application/json"
        body: |
          {{
            "name": "{device_name}",
            "node_type": "{node_type}",
            "compute_id": "{{{{ compute_id }}}}",
            "x": {x_coord},
            "y": {y_coord},
            "symbol":"{symbol}",
            "template_id": "{template_id}"
          }}
        body_format: json
        return_content: yes
        status_code: 201
      register: switch_result

    - name: Debug {machine} creation result
      debug:
        var: switch_result
"""
        # Update x-coordinate for next device
        x_coord += x_step

    # Write the generated YAML content to the output file
    with open(output_file, 'w') as file:
        file.write(yaml_content)
    
    print(f"YAML file has been generated: {output_file}")

def main():
    # Path to the machine_info.txt file
    machine_info_file = os.path.expanduser("~/Documents/VSCodeProjects/machine_names.txt")
    # Output YAML file
    output_yaml_file = os.path.expanduser("~/Documents/VSCodeProjects/generated_topology.yaml")
    
    # Read the saved VSDX file path and get the project name
    vsdx_file_path = read_vsdx_path()
    project_name = get_project_name_from_vsdx(vsdx_file_path)
    
    # Read machine information
    machine_info = read_machine_info(machine_info_file)
    
    # Generate the YAML file with the specified project name
    generate_yaml(machine_info, output_yaml_file, project_name)

if __name__ == "__main__":
    main()
