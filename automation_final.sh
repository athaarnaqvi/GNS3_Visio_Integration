#!/bin/bash
echo "Extracting files"
python3 extract_vsdx.py
echo "Extracting Machine Names"
python3 machine_info.py
echo "Generating Ansible-Playbook"
python3 gns3_yaml.py
echo "Extracting Connection"
python3 ListConnections.py
python3 addportnumbers.py
echo "Generating Playbook"
python3 generatePlaybook.py
echo "Running Playbooks"
ansible-playbook generated_topology.yaml
ansible-playbook generated_playbook.yaml
