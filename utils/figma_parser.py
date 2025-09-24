def extract_relevant_nodes(node, parent_name=None, types=('FRAME', 'TEXT', 'COMPONENT', 'INSTANCE'), collected=None):
    if collected is None:
        collected = []

    node_type = node.get('type')
    node_id = node.get('id')
    node_name = node.get('name', '')
    text = node.get('characters') if node_type == 'TEXT' else None

    if node_type in types:
        extracted = {
            'id': node_id,
            'name': node_name,
            'type': node_type,
            'text': text,
            'parent': parent_name,
            'styles': node.get('styles', {}),
            'style': node.get('style', {}),  # useful for TEXT nodes (fontSize, fontFamily, etc.)
            'fills': node.get('fills', []),
            'strokes': node.get('strokes', []),
            'effects': node.get('effects', []),
            'absoluteBoundingBox': node.get('absoluteBoundingBox', None),
            'layoutMode': node.get('layoutMode', None),
            'constraints': node.get('constraints', None)
        }

        collected.append(extracted)

    # Recurse into children
    for child in node.get('children', []):
        extract_relevant_nodes(child, parent_name=node_name, types=types, collected=collected)

    return collected
