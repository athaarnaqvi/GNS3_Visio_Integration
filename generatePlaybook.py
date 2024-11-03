import json
import os

def read_vsdx_path():
    """Read the saved VSDX file path from the 'vsdx_path' file."""
    with open("vsdx_path.txt", "r") as file:
        vsdx_file_path = file.read().strip()
    return vsdx_file_path

def get_project_name_from_vsdx(vsdx_path):
    """Extract the project name from the VSDX file name without the extension."""
    return os.path.splitext(os.path.basename(vsdx_path))[0]

def generate_ansible_playbook(connections_file, project_name, gns3_server="http://localhost:3080"):
    # Load the JSON data
    with open(connections_file, 'r') as file:
        connections = json.load(file)
    
    # Start creating the playbook content
    playbook = f"""---
- name: Create links in GNS3 project based on JSON file
  hosts: localhost
  gather_facts: no
  vars:
    gns3_server: "{gns3_server}"
    project_name: "{project_name}"
    
  tasks:
    - name: Get all projects from GNS3
      uri:
        url: "{{{{ gns3_server }}}}/v2/projects"
        method: GET
        return_content: yes
      register: gns3_projects

    - name: Set project ID based on project name
      set_fact:
        project_id: "{{{{ (gns3_projects.json | selectattr('name', 'equalto', project_name) | list)[0].project_id }}}}"
      when: gns3_projects.json | selectattr('name', 'equalto', project_name) | list | length > 0
      
    - name: Check if the project is opened
      uri:
        url: "{{{{ gns3_server }}}}/v2/projects/{{{{ project_id }}}}"
        method: GET
        return_content: yes
      register: project_status

    - name: Open the project if it is not already opened
      uri:
        url: "{{{{ gns3_server }}}}/v2/projects/{{{{ project_id }}}}/open"
        method: POST
        return_content: yes
        status_code: [200, 201]
      when: project_status.json.status != "opened"
      
    - name: Retrieve device node IDs from the GNS3 project
      uri:
        url: "{{{{ gns3_server }}}}/v2/projects/{{{{ project_id }}}}/nodes"
        method: GET
        return_content: yes
      register: gns3_nodes
    """

    # Add the tasks for creating the links
    for connection in connections:
        from_device = connection['from']
        to_device = connection['to']
        from_port_number = connection['from_port_number']
        to_port_number = connection['to_port_number']
        
        playbook += f"""
    - name: Create link from {from_device} to {to_device}
      vars:
        device_map: "{{{{ gns3_nodes.json | items2dict(key_name='name', value_name='node_id') }}}}"
      uri:
        url: "{{{{ gns3_server }}}}/v2/projects/{{{{ project_id }}}}/links"
        method: POST
        body_format: json
        headers:
          Content-Type: application/json
        status_code: [200, 201]
        body:
          nodes:
          - node_id: "{{{{ device_map['{from_device}'] }}}}"
            adapter_number: 0
            port_number: {from_port_number}
          - node_id: "{{{{ device_map['{to_device}'] }}}}"
            adapter_number: 0
            port_number: {to_port_number}
        """
    
    return playbook


# Example usage:
if __name__ == "__main__":
    connections_file = os.path.expanduser("~/Documents/VSCodeProjects/connections.json")  # path to your JSON file

    vsdx_file_path = read_vsdx_path()
    project_name = get_project_name_from_vsdx(vsdx_file_path)

    ansible_playbook = generate_ansible_playbook(connections_file, project_name)

    # Write the playbook to a YAML file
    with open('generated_playbook.yml', 'w') as file:
        file.write(ansible_playbook)

    print("Ansible playbook generated successfully.")

