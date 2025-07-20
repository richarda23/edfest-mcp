import json
import os
from typing import Dict, List

from fastmcp import FastMCP
import edfestcli


cli = edfestcli.EdFestCli()


mcp = FastMCP("My MCP Server")


@mcp.tool(description="Search Edinburgh festival venues")
def edinburgh_festival_venues(
    festival: str = "international",
    postcode: str = None,
    name: str = None,
    year: str = "2025",
) -> List[Dict]:
    """
    Searches Edinburgh festival venues.
    :param festival: The type of festival to search for venues in.
    :param postcode: The postcode to filter venues by.
    :param name: The name of the venue to search for.
    :param year: The year of the festival.
    :return: A dictionary containing venue information.
    """
    params = {
        "festival": festival,
        "year": year,
        "postcode": postcode,
        "name": name,
    }
    filtered_params = {k: v for k, v in params.items() if v}

    results = cli.venues(filtered_params)
    return results


@mcp.tool()
def edinburgh_festival_events(
    datetime_from="2025-01-01 00:00:00",
    datetime_to="2025-12-31 23:59:59",
    festival="international",
    genre=None,
    venue_name=None,
    search_text=None,
    title=None,
    artist=None,
    year="*",
) -> List[Dict]:
    """
    Searches this year's Edinburgh festival events.
    :param datetime_from: An optional ISO8601-like timestamp. e.g. '2025-08-12 00:00:00'
    :param datetime_to:  An optional ISO8601-like timestamp. e.g. '2025-08-12 00:00:00'
    :param festival:  possible values are fringe, demofringe, jazz, book, international, tattoo, art, hogmanay, science, imaginate, film, mela, storytelling.
    :param genre: The genre of the show. This will vary by festival type but may include comedy, theatre etc
    :param venue_name: The genre of the show. This will vary by festival type but may include comedy, theatre etc
    :param search_text:  description  of the show to search for.
    :param artist:  Name of an artist or performer to search for.
    :param title: the title of the show to search for.
    :param year: The year of the festival. Defaults to "*", which means all years.
    :return:
    """
    params = {
        "festival": festival,
        "year": year,
        "date_from": datetime_from.replace("T", " "),
        "date_to": datetime_to.replace("T", " "),
        "genre": genre,
        "venue_name": venue_name,
        "description": search_text,
        "artist": artist,
        "title": title,
    }
    ## If year is "*", we remove the date filters
    if year == "*":
        del params["date_from"]
        del params["date_to"]
    filtered_params = {k: v for k, v in params.items() if v}

    results = cli.events(filtered_params)
    # for r in results:
    #     del r['images']
    return results


if __name__ == "__main__":
    mcp.run()
