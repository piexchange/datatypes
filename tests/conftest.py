
def pytest_make_parametrize_id(config, val, argname):
    if getattr(val, '__module__', None) == 'typing':
        return str(val)[7:]

    if callable(val):
        return val.__name__
