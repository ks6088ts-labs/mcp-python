[![test](https://github.com/ks6088ts-labs/mcp-python/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/mcp-python/actions/workflows/test.yaml?query=branch%3Amain)
[![docker](https://github.com/ks6088ts-labs/mcp-python/actions/workflows/docker.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/mcp-python/actions/workflows/docker.yaml?query=branch%3Amain)
[![docker-release](https://github.com/ks6088ts-labs/mcp-python/actions/workflows/docker-release.yaml/badge.svg)](https://github.com/ks6088ts-labs/mcp-python/actions/workflows/docker-release.yaml)
[![ghcr-release](https://github.com/ks6088ts-labs/mcp-python/actions/workflows/ghcr-release.yaml/badge.svg)](https://github.com/ks6088ts-labs/mcp-python/actions/workflows/ghcr-release.yaml)
[![docs](https://github.com/ks6088ts-labs/mcp-python/actions/workflows/github-pages.yaml/badge.svg)](https://github.com/ks6088ts-labs/mcp-python/actions/workflows/github-pages.yaml)

# mcp-python

This is a template repository for Python

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [GNU Make](https://www.gnu.org/software/make/)

## Install MCP Server on Cline

This repository contains a Python implementation of the Model Context Protocol (MCP) server. To install the MCP server, follow these steps:

1. Clone the repository:

```bash
# Clone the repository
git clone https://github.com/ks6088ts-labs/mcp-python.git
cd mcp-python

# Install dependencies
make install-deps-dev

# (Optional) Confirm MCP server is working
# You can run the MCP server locally to test it.
uv run python scripts/weather.py
```

2. Install the MCP server on Cline:

To install the MCP server on Cline, you need to create a configuration file like ``/PATH/TO/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` in your Cline user directory. The configuration file should contain the following:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/Users/ks6088ts/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/ks6088ts/src/github.com/ks6088ts-labs/mcp-python/scripts",
        "run",
        "weather.py"
      ]
    }
  }
}
```

You can see the settings just like screenshots below:

![cline_configure_mcp_server](./docs/images/cline_configure_mcp_server.png)

3. Try it out from Cline:

## ![cline_run_mcp_server](./docs/images/cline_run_mcp_server.gif)

## References

- [Model Context Protocol (MCP) > Quickstart > For Server Developers](https://modelcontextprotocol.io/quickstart/server)
