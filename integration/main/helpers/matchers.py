from hamcrest import all_of, contains_inanyorder, has_entries, has_key, instance_of, not_none, not_

__all__ = [
    'has_keys',
    'has_only_entries',
    'has_only_keys',
    'not_empty'
]


def has_keys(*keys):
    return all_of(*[has_key(k) for k in keys])


def has_only_entries(**kwargs):
    return all_of(instance_of(dict),
                  contains_inanyorder(*kwargs.keys()),
                  has_entries(**kwargs))


def has_only_keys(*keys):
    return all_of(instance_of(dict),
                  contains_inanyorder(*keys))


def not_empty():
    return all_of(
        not_none(),
        not_('')
    )
