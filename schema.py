DGRAPH_SCHEMA = """
    id: string .
    external_id: string .
    name: string  @index(term) .
    parent: uid .
    children: [uid] @count .
    instanceof: [uid] @count .
    attributes: [uid] @count .

    type object {
        id
        external_id
        name
        parent
        children
        instanceof
        attributes
    }

    name: string  @index(term) .
    category: string @index(term) .
    value: string .
    data_type: int .
    data_type_context: string .
    display_name: string @index(term) .
    flags: int .
    display_precision: int .

    type attribute {
        name
        category
        value
        data_type
        data_type_context
        display_name
        flags
        display_precision
    }
    """

def get_schema():
    return DGRAPH_SCHEMA
