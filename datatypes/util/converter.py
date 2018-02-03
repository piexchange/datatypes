
import inspect


def converter(func):
    """
    Marks a function as the equivalent of the Type.convert method.
    Can be used on arbitrary types to make them convertable.

    Example:
    ::
        class MyClass:
            @converter
            @classmethod
            def parse(cls, value):
                return cls()

        # the following line wouldn't work without the annotation
        List(MyClass).convert("a,b,c")

    An annotated method in a child class takes precedence over annotated methods in parent classes.
    If multiple methods are annotated in the same class, it's undefined which one of them will be used.

    :param func: The function to use in place of the `convert` method
    """

    frame = inspect.currentframe().f_back
    frame.f_locals['_converter_func'] = func
    del frame
    return func
