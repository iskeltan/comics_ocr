comics_mapping = {

    'properties': {
        'id': {'type': 'integer', 'store': True},
        'content': {'type': 'keyword', 'split_queries_on_whitespace': True, 'index': True},
        'tags': {'type': 'keyword', 'split_queries_on_whitespace': True}
    }
}