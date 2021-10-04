"""Tests standard tap features using the built-in SDK tests library."""

import json
from singer_sdk.testing import get_standard_tap_tests
from tap_callrail.tap import Tapcallrail

SAMPLE_CONFIG = {}

with open(".secrets/config.json") as f:
    contents = f.read()
    SAMPLE_CONFIG = json.loads(contents)

# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(
        Tapcallrail,
        config=SAMPLE_CONFIG
    )
    for test in tests:
        test()


# TODO: Create additional tests as appropriate for your tap.
