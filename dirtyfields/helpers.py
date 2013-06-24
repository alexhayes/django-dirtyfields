
def get_changes(instance, dirty_fields=None):
    """
    Get a dict of changes with existing and new values.
    
    @param instance:     The instance to get changes on.
    @param dirty_fields: If supplied this dict will be used as dirty fields 
                         rather than instance.get_dirty_fields().
    @return dict         A dict of field names which each consist of a dict 
                         containing keys 'existing' and 'new'.
    """
    changes = {}
    if dirty_fields is None:
        dirty_fields = instance.get_dirty_fields()
    for field, old in dirty_fields.iteritems():
        changes[field] = {'existing': old, 'new': getattr(instance, field)}
    return changes