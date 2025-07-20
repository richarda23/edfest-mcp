import json
from typing import Dict

from fastmcp import FastMCP
import edfestcli


def call_edfest_api() -> Dict:
    cli = edfestcli.EdFestCli()
    return cli.events({"year": "2025"})


def main():
    print("Hello from edfringe-mcp!")


mcp = FastMCP("My MCP Server")


@mcp.tool()
def search_edinburgh_festivals(
    datetime_from="2025-09-01",
    datetime_to="2025-09-01",
    festival="international",
    genre=None,
    venue_name=None,
    search_text=None,
    title=None,
    artist=None,
):
    """
    Searches this year's Edinburgh festival events.
    :param datetime_from: An optional ISO8601-like timestamp. e.g. '2025-08-12 00:00:00'
    :param datetime_to:  An optional ISO8601-like timestamp. e.g. '2025-08-12 00:00:00'
    :param festival:  possible values are fringe, demofringe, jazz, book, international, tattoo, art, hogmanay, science, imaginate, film, mela, storytelling]
    :param genre: The genre of the show. This will vary by festival type but may include comedy, theatre etc
    :param venue_name: The genre of the show. This will vary by festival type but may include comedy, theatre etc
    :param search_text:  description  of the show to search for.
    :param artist:  Name of an artist or performer to search for.
    :param title: the title of the show to search for.
    :return:
    """
    params = {
        "festival": festival,
        "year": "2025",
        "date_from": datetime_from.replace("T", " "),  # optional
        "date_to": datetime_to.replace("T", " "),  # not included if None
        "genre": genre,
        "venue_name": venue_name,
        "description": search_text,
        "artist": artist,
        "title": title,
    }
    filtered_params = {k: v for k, v in params.items() if v}

    cli = edfestcli.EdFestCli()
    results = cli.events(filtered_params)
    # for r in results:
    #     del r['images']
    return results


if __name__ == "__main__":
    print("Starting edfringe-mcp..." + mcp.name)
    mcp.run()
