
def pytest_make_parametrize_id(config, val, argname):
    if getattr(val, '__module__', None) == 'typing':
        if hasattr(val, '__name__'):
            return val.__name__

        return str(val)[7:]

    if callable(val):
        return val.__name__

    if isinstance(val, list):
        return repr(val)

    if isinstance(val, str):
        return repr(val)
