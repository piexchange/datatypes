
def pytest_make_parametrize_id(config, val, argname):
    if getattr(val, '__module__', None) == 'typing':
        return str(val).replace('typing.', '')

    if callable(val):
        return val.__name__

    if isinstance(val, list):
        return repr(val)

    if isinstance(val, str):
        return repr(val)
