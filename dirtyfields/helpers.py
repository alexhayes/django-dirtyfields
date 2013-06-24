
def get_changes(instance):
    """
    Get a dict of changes with existing and new values.
    """
    changes = {}
    for field, old in instance.get_dirty_fields().iteritems():
        changes[field] = {'existing': old, 'new': getattr(instance, field)}
    return changes