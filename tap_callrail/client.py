"""REST client handling, including callrailStream base class."""

import datetime
import requests
from pathlib import Path
from typing import Any, Dict, Optional, List, Iterable
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class callrailStream(RESTStream):
    """callrail stream class."""

    records_jsonpath = "$.calls[*]"        
    next_page_token_jsonpath = "$.page"
    page_total_token_jsonpath = "$.total_pages"

    sorting_field: Optional[str] = None
    _field_selections: List[str] = []

    @property
    def url_base(self) -> str:
        """Return the base url, e.g. 'https://api.mysite.com/v3/'."""
        return f"https://api.callrail.com/v3/a/{self.config.get('account_id')}"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Authorization",
            value=f'Token token="{self.config.get("api_key")}"',
            location="header"
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        current_page_match = extract_jsonpath(
            self.next_page_token_jsonpath, response.json()
        )
        current_total_page_match = extract_jsonpath(
            self.page_total_token_jsonpath, response.json()
        )
        first_current_page_match = next(iter(current_page_match), None)
        first_page_total_match = next(iter(current_total_page_match), None)
        if first_current_page_match >= first_page_total_match:
            return None

        return first_current_page_match + 1

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["per_page"] = self.config.get("per_page", 250)
        if next_page_token:
            params["page"] = next_page_token
        starting_date = self.get_starting_timestamp(context)
        if starting_date:
            # We wan't only those after the starting date so we add a second, although this is pretty hacky
            params["start_date"] = (starting_date + datetime.timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S")
        field_selections = self.get_list_of_non_optionals()
        if field_selections:
            params["fields"] = ",".join(field_selections)
        if self.sorting_field:
            params["sorting"] = self.sorting_field
            params["order"] = "asc"
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def get_list_of_non_optionals(self) -> List[str]:
        if not self._field_selections:
            required = self.schema["required"]
            properties = self.schema["properties"].keys()
            self._field_selections = list(set(properties) - set(required))
        return self._field_selections
