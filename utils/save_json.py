import json
from .figma_parser import extract_relevant_nodes
import config

def process_figma_response(response: dict):
    node_id = list(response['nodes'].keys())[0]
    root_node = response['nodes'][node_id]['document']

    filtered_nodes = extract_relevant_nodes(root_node)
    output_filepath=f"{config.ISSUE_KEY}_figma_data.json"
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(filtered_nodes, f, indent=4)

    print(f"Extracted {len(filtered_nodes)} relevant nodes.")
    return filtered_nodes

