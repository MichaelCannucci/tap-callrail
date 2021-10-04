# tap-callrail

`tap-callrail` is a Singer tap for callrail.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

- [ ] `Developer TODO:` Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

```bash
# TODO: Create PyPi Repo
pipx install tap-callrail
```

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```
"api_key": The key to authenticate against the API service (Required)
"account_id": Callrail account id (Required)
"start_date": The earliest record date to sync
"per_page": Number of records to fetch per page (max: 250)
```
or
```bash
tap-callrail --about
```

## Usage

You can easily run `tap-callrail` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-callrail --version
tap-callrail --help
tap-callrail --config CONFIG --discover > ./catalog.json
```

## Developer Resources

API Resources for the CallRail API are available on their documentation
```
https://apidocs.callrail.com/#sorting
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create a config.json in .secrets and fill out the tap settings

```
{
    "api_key": "API_KEY_HERE",
    "account_id": "ACCOUNT_ID_HERE",
    "start_date": "2021-10-01"
}
```

Create tests within the `tap_callrail/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-callrail` CLI interface directly using `poetry run`:

```bash
poetry run tap-callrail --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-callrail
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-callrail --version
# OR run a test `elt` pipeline:
meltano elt tap-callrail target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.
