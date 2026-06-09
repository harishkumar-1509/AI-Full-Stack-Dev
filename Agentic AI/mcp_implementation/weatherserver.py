from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")


@mcp.tool()
def get_weather(city: str) -> str:
    """Returns the weather description for the given city.

    Args:
        city (str): The city name to get weather for.

    Returns:
        str: A static weather string mentioning the city.
    """
    return f"Sunny and warm in {city}"


if __name__ == "__main__":
    # Run using the streamable-http transport so the MCP transport is streamable HTTP
    mcp.run(transport="streamable-http")
