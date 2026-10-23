# Alexa-Concierge-Streamable-MCP-Bridge
Self-hosted Streamable HTTP MCP server (spec 2025-11-25) &amp; interactive web simulator for Alexa+ agentic tools
# Alexa+ Smart Concierge & MCP Server

A full-stack agentic integration for **Alexa+** built in accordance with the official **MCP Spec (2025-11-25, Streamable HTTP)**, integrated with an interactive simulated web application interface.

## Track & Challenge Entries
- **Primary Track:** Alexa+
- **Mini Challenge:** AWS Builder (Integrated with AWS AgentCore and Bedrock model-dispatch patterns)

## System Overview
- **MCP Protocol Conformance:** Exposes streamable HTTP tools for dynamic tool calling via `/mcp/tools` and `/mcp/call`.
- **Agentic Workflow:** Simulates Alexa+ conversational routing to discover local connected nodes, read device metrics, and trigger automation protocols.
- **Web Simulation Layer:** Includes a zero-setup browser interface testing tool invocation and responses in real time.

## Quickstart

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
