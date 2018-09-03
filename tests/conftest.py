
import pytest


def depends_on(*parent_tests):
    def mark(child_test):
        child_test.parent_tests = parent_tests
        return child_test

    return mark


# def pytest_collection_modifyitems(config, items):
#     for item in items:
#         item.function.items = {item}

# def pytest_configure(config):
#     # register an additional marker
#     config.addinivalue_line("markers", "depends_on(*parent_tests): skip test if any of the parent tests failed")


# def pytest_runtest_makereport(item, call):
#     item.function.failed = call.excinfo is not None
#     print('makereport:', item.function, item.function.failed)


# def pytest_runtest_setup(item):
#     parent_tests = getattr(item.function, 'parent_tests', [])
#     print('runtest_setup:', item, parent_tests, [parent.failed for parent in parent_tests])
#     if any(parent.failed for parent in parent_tests):
#         pytest.skip("parent test failed")

