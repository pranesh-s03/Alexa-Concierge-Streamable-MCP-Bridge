import json
import asyncio
from aiohttp import web

# MCP Protocol Implementation (Spec: 2025-11-25 / Streamable HTTP)
TOOLS_SCHEMA = [
    {
        "name": "check_device_telemetry",
        "description": "Reads real-time operational status and metrics from Amazon smart home devices.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "device_id": {"type": "string", "description": "Identifier for the target device"}
            },
            "required": ["device_id"]
        }
    },
    {
        "name": "trigger_security_protocol",
        "description": "Executes home perimeter check and locks external access nodes via AWS runtime integration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "zone": {"type": "string", "description": "Target zone (e.g., perimeter, entrance, living_room)"}
            },
            "required": ["zone"]
        }
    }
]

INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Alexa+ Agentic Smart Concierge</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 2rem; display: flex; flex-direction: column; align-items: center; }
    .card { background: #1e293b; border-radius: 12px; padding: 2rem; width: 100%; max-width: 600px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    h1 { font-size: 1.5rem; margin-top: 0; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
    .status-badge { display: inline-block; background: #0284c7; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; }
    .log-container { background: #0b0f19; border-radius: 8px; padding: 1rem; height: 200px; overflow-y: auto; font-family: monospace; font-size: 0.85rem; margin-top: 1rem; border: 1px solid #334155; }
    button { background: #38bdf8; color: #0f172a; border: none; padding: 10px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 1rem; }
    button:hover { background: #7dd3fc; }
  </style>
</head>
<body>
  <div class="card">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h1>Alexa+ Concierge</h1>
      <span class="status-badge">MCP Spec 2025-11-25 Connected</span>
    </div>
    <p style="color: #94a3b8; font-size: 0.9rem;">Self-Hosted Streamable HTTP MCP Agent for Alexa+ Environment.</p>
    <div>
      <button onclick="runMcpTool('check_device_telemetry', {device_id: 'echo-hub-01'})">Query Echo Hub Status</button>
      <button onclick="runMcpTool('trigger_security_protocol', {zone: 'perimeter'})">Trigger Perimeter Protocol</button>
    </div>
    <div class="log-container" id="terminal">
      <div>[system] MCP server stream initialized over HTTP...</div>
      <div>[alexa+] Listening for agentic intent calls...</div>
    </div>
  </div>

  <script>
    async function runMcpTool(toolName, args) {
      const term = document.getElementById('terminal');
      term.innerHTML += `<div style="color:#fde047;">> Alexa+ invoking tool: ${toolName}...</div>`;
      try {
        const res = await fetch('/mcp/call', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({name: toolName, arguments: args})
        });
        const data = await res.json();
        term.innerHTML += `<div style="color:#4ade80;">[mcp response] ${JSON.stringify(data.result)}</div>`;
      } catch (err) {
        term.innerHTML += `<div style="color:#f87171;">[error] ${err.message}</div>`;
      }
      term.scrollTop = term.scrollHeight;
    }
  </script>
</body>
</html>
"""

async def handle_index(request):
    return web.Response(text=INDEX_HTML, content_type='text/html')

async def handle_mcp_discovery(request):
    """Alexa+ MCP Tool Discovery Endpoint"""
    return web.json_response({
        "protocolVersion": "2025-11-25",
        "transport": "streamable-http",
        "tools": TOOLS_SCHEMA
    })

async def handle_mcp_call(request):
    """Alexa+ Tool Execution Dispatcher"""
    payload = await request.json()
    tool_name = payload.get("name")
    args = payload.get("arguments", {})

    if tool_name == "check_device_telemetry":
        result = {
            "device": args.get("device_id"),
            "status": "ONLINE",
            "battery": "98%",
            "network_latency": "14ms",
            "aws_agentcore_routed": True
        }
    elif tool_name == "trigger_security_protocol":
        result = {
            "zone": args.get("zone"),
            "status": "ENGAGED",
            "locks_verified": True,
            "timestamp": "2026-10-23T22:00:00Z"
        }
    else:
        result = {"error": f"Unknown tool: {tool_name}"}

    return web.json_response({"result": result})

app = web.Application()
app.router.add_get('/', handle_index)
app.router.add_get('/mcp/tools', handle_mcp_discovery)
app.router.add_post('/mcp/call', handle_mcp_call)

if __name__ == '__main__':
    web.run_app(app, port=8080)
