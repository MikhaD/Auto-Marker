import tests.test_is_type
import doctest

total = 0
failed = 0

results = doctest.testmod(tests.test_is_type)
total += results.attempted
failed += results.failed

print(f"Passed {total - failed}/{total} tests")