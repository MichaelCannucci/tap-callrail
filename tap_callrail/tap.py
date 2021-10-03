"""callrail tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_callrail.streams import (
    CallsStream,
)

STREAM_TYPES = [
    CallsStream,
]

class Tapcallrail(Tap):
    """callrail tap class."""
    name = "tap-callrail"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="The key to authenticate against the API service"
        ),
        th.Property(
            "account_id",
            th.StringType,
            required=True,
            description="Callrail account id"
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync"
        ),
        th.Property(
            "per_page",
            th.IntegerType,
            description="Number of records to fetch per page"
        )
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
