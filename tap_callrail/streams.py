"""Stream type classes for tap-callrail."""

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_callrail.client import SCHEMAS_DIR, callrailStream

class CallsStream(callrailStream):
    """Calls stream."""
    name = "calls"
    path = "/calls.json"
    primary_keys = ["id"]
    sorting_field = "start_time"
    replication_key = "start_time"
    schema_filepath = SCHEMAS_DIR / "calls.json"