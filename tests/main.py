import unittest

tests = unittest.TestLoader().discover(
    "tests", pattern="*_tests.py", top_level_dir=None
)
unittest.TextTestRunner(verbosity=2).run(tests)
