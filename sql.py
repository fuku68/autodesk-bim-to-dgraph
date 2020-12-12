OBJECTS_SQL = """
    SELECT _objects_id.*, _objects_val.value
    FROM _objects_id
    LEFT JOIN _objects_eav
    ON _objects_id.id = _objects_eav.entity_id
    LEFT JOIN _objects_val
    ON _objects_val.id = _objects_eav.value_id
    LEFT JOIN _objects_attr
    ON _objects_attr.id = _objects_eav.attribute_id
    WHERE _objects_attr.category = '__name__'
    """

CHILD_SQL = """
    SELECT _objects_id.id, _objects_val.value
    FROM _objects_id
    LEFT JOIN _objects_eav
    ON _objects_id.id = _objects_eav.entity_id
    LEFT JOIN _objects_val
    ON _objects_val.id = _objects_eav.value_id
    LEFT JOIN _objects_attr
    ON _objects_attr.id = _objects_eav.attribute_id
    WHERE _objects_attr.category = '__child__'
    """

PARRENT_SQL = """
    SELECT _objects_id.id, _objects_val.value
    FROM _objects_id
    LEFT JOIN _objects_eav
    ON _objects_id.id = _objects_eav.entity_id
    LEFT JOIN _objects_val
    ON _objects_val.id = _objects_eav.value_id
    LEFT JOIN _objects_attr
    ON _objects_attr.id = _objects_eav.attribute_id
    WHERE _objects_attr.category = '__parent__'
    """

INSTANCEOF_SQL = """
    SELECT _objects_id.id, _objects_val.value
    FROM _objects_id
    LEFT JOIN _objects_eav
    ON _objects_id.id = _objects_eav.entity_id
    LEFT JOIN _objects_val
    ON _objects_val.id = _objects_eav.value_id
    LEFT JOIN _objects_attr
    ON _objects_attr.id = _objects_eav.attribute_id
    WHERE _objects_attr.category = '__instanceof__'
    """

ATTRIBUTES_SQL = """
    SELECT _objects_eav.entity_id,
        _objects_attr.name, _objects_attr.category,
        _objects_attr.data_type, _objects_attr.data_type_context,
        _objects_attr.display_name, _objects_attr.flags,
        _objects_attr.display_precision, _objects_val.value
    FROM _objects_attr
    LEFT JOIN _objects_eav
    ON _objects_attr.id = _objects_eav.attribute_id
    LEFT JOIN  _objects_val
    ON _objects_val.id = _objects_eav.value_id
    WHERE _objects_attr.category != '__name__'
    AND _objects_attr.category != '__child__'
    AND _objects_attr.category != '__parent__'
    AND _objects_attr.category != '__instanceof__'
    """
