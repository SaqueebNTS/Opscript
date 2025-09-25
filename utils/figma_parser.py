def extract_relevant_nodes(node, parent_name=None, types=('FRAME', 'TEXT', 'COMPONENT', 'INSTANCE'), collected=None):
    if collected is None:
        collected = []

    node_type = node.get('type')
    node_id = node.get('id')
    node_name = node.get('name', '')
    text = node.get('characters') if node_type == 'TEXT' else None

    if node_type in types:
        # Simplified extracted data
        extracted = {
            'id': node_id,
            'name': node_name,
            'type': node_type,
            'text': text,  # Only for TEXT nodes
            'parent': parent_name,
            'styles': {k: node.get('styles', {}).get(k) for k in ['grid']},  # Only keep 'grid' for styles
            'fills': [],  # Default to an empty list
            'layoutMode': node.get('layoutMode'),
            'constraints': {k: node.get('constraints', {}).get(k) for k in ['vertical', 'horizontal']}  # Only keep the constraints
        }

        # Check if 'fills' exists and is not empty
        fills = node.get('fills', [])
        if fills:
            # Only keep the first fill color, and convert to 'rgba'
            first_fill = fills[0].get('color', {})
            extracted['fills'] = [{
                "color": f"rgba({int(first_fill.get('r', 0) * 255)}, "
                         f"{int(first_fill.get('g', 0) * 255)}, "
                         f"{int(first_fill.get('b', 0) * 255)}, "
                         f"{first_fill.get('a', 1)})"
            }]
        
        # Append to the collected list
        collected.append(extracted)

    # Recurse into children (if any)
    for child in node.get('children', []):
        extract_relevant_nodes(child, parent_name=node_name, types=types, collected=collected)

    return collected
