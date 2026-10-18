import hashlib
import os

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request

EMAIL = "23f1000183@ds.study.iitm.ac.in"

mcp = FastMCP("Exam Challenge Server")


@mcp.tool()
def solve_challenge() -> str:
    """Calculate the response using the current HTTP challenge header."""
    request = get_http_request()
    challenge = request.headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    return hashlib.sha256(
        f"{challenge}:{EMAIL}".encode("utf-8")
    ).hexdigest()[:16]


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        stateless_http=True,
    )