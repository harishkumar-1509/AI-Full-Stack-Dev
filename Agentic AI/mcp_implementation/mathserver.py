from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """_summary_
    Add two numbers
    Args:
        a (int): first number
        b (int): second number

    Returns:
        int: sum of two numbers
    """
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """_summary_
    Multiply two numbers
    Args:
        a (int): first number
        b (int): second number

    Returns:
        int: product of two numbers
    """
    return a * b


# "stdio": tells the server to use standard i/p and o/p to receive and respond to tool function calls.
if __name__ == "__main__":
    mcp.run(transport="stdio")
