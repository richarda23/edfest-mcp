# edfringe-mcp

An MCP server to query the Edinburgh Festivals API for information about events and venues for all the Edinburgh festivals, inluding historical data.

Note that access to  Fringe event data for 2025 is not yet supported; this requires approval.

<a href="https://glama.ai/mcp/servers/@richarda23/edfest-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@richarda23/edfest-mcp/badge" alt="Edinburgh Festivals Server MCP server" />
</a>

## Tools

- `search_edinburgh_festivals`: Search for events based on location, genre, date, or text.
- `search_edinburgh_festival_venues`: Search for venues based on festival type, postcode or other criteria.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/#highlights)

## Setup

1. [Create an Edinburgh Festival API account](https://api.edinburghfestivalcity.com/documentation).

2. Clone or download this project.  
   Create a `.env` file in the project root containing:
    ```
    api_secret=your_secret
    api_key=your_key
    ```

    If you have a Google Maps API key you can add

    ```
    GOOGLE_MAPS_API_KEY=your API key
    ```
    and that will enable timing and route calculations between venues. 

3. Install dependencies:
    ```
    uv sync
    ```

4. Add the following MCP configuration to your `mcp.json` config file in your LLM client app:
    ```json
    "edinburghFestival": {
        "command": "uv",
        "args": [
            "--directory",
            "/full/path/to/edfringe-mcp",
            "run",
            "main.py"
        ]
    }
    ```

## Development

Running tests:

    uv sync --all-groups
    uv run pytest

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.