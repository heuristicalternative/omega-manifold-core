//! HEADER LAYER: L3 - Protocol Actuation & Tool Brokerage
//! Implementation of the Model Context Protocol (MCP) JSON-RPC 2.0 Specification.
//! Enables automated, secure multi-tenant filesystem mutations within the workspace.

use serde::{Deserialize, Serialize};
use serde_json::json;
use std::path::{Path, PathBuf};
use tokio::fs;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};

#[derive(Debug, Serialize, Deserialize)]
struct JsonRpcRequest {
    jsonrpc: String,
    method: String,
    #[serde(default)]
    params: serde_json::Value,
    id: serde_json::Value,
}

const WORKSPACE_ROOT: &str = "/home/dante/omega-manifold";

/// Verifies that a relative or absolute target path resides strictly inside the workspace bounds
fn safe_resolve_path(raw_path: &str) -> Result<PathBuf, &'static str> {
    let base = Path::new(WORKSPACE_ROOT);
    let target = if Path::new(raw_path).is_absolute() {
        PathBuf::from(raw_path)
    } else {
        base.join(raw_path)
    };

    // Canonicalize paths if they exist to strip potential ".." traversal attacks
    if let Ok(canonical) = target.canonicalize() {
        if canonical.starts_with(base) {
            return Ok(canonical);
        }
    } else {
        // If file doesn't exist yet, check the ancestry chain structurally
        let mut current = target.as_path();
        while let Some(parent) = current.parent() {
            if parent == base {
                return Ok(target);
            }
            current = parent;
        }
    }
    Err("Security Exception: Operation attempted outside authorized workspace boundary.")
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let stdin = tokio::io::stdin();
    let mut stdout = tokio::io::stdout();
    let mut reader = BufReader::new(stdin).lines();

    while let Some(line) = reader.next_line().await? {
        if let Ok(req) = serde_json::from_str::<JsonRpcRequest>(&line) {
            let response = match req.method.as_str() {
                "initialize" => json!({
                    "jsonrpc": "2.0",
                    "id": req.id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": { "name": "omega-mcp-bridge", "version": "16.78.2" }
                    }
                }),
                "tools/list" => json!({
                    "jsonrpc": "2.0",
                    "id": req.id,
                    "result": {
                        "tools": [
                            {
                                "name": "mutate_manifold_state",
                                "description": "Writes production source files directly into localized workspace targets securely.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "module_path": { "type": "string" },
                                        "payload_raw": { "type": "string" }
                                    },
                                    "required": ["module_path", "payload_raw"]
                                }
                            }
                        ]
                    }
                }),
                "tools/call" => {
                    let tool_name = req.params.get("name").and_then(|v| v.as_str()).unwrap_or("");
                    let arguments = req.params.get("arguments").cloned().unwrap_or(json!({}));
                    
                    if tool_name == "mutate_manifold_state" {
                        let mod_path = arguments.get("module_path").and_then(|v| v.as_str()).unwrap_or("");
                        let payload = arguments.get("payload_raw").and_then(|v| v.as_str()).unwrap_or("");
                        
                        match safe_resolve_path(mod_path) {
                            Ok(resolved) => {
                                // Enforce defensive pre-creation invariant natively
                                if let Some(parent) = resolved.parent() {
                                    let _ = fs::create_dir_all(parent).await;
                                }
                                match fs::write(&resolved, payload).await {
                                    Ok(_) => json!({
                                        "jsonrpc": "2.0",
                                        "id": req.id,
                                        "result": { "content": [{ "type": "text", "text": "File state successfully materialized." }] }
                                    }),
                                    Err(e) => json!({
                                        "jsonrpc": "2.0",
                                        "id": req.id,
                                        "error": { "code": -32001, "message": format!("Filesystem I/O Write failure: {}", e) }
                                    })
                                }
                            }
                            Err(err_msg) => json!({
                                "jsonrpc": "2.0",
                                "id": req.id,
                                "error": { "code": -32000, "message": err_msg }
                            })
                        }
                    } else {
                        json!({
                            "jsonrpc": "2.0",
                            "id": req.id,
                            "error": { "code": -32601, "message": "Unknown tool invocation method." }
                        })
                    }
                },
                _ => json!({
                    "jsonrpc": "2.0",
                    "id": req.id,
                    "error": { "code": -32601, "message": "Method lookup non-existent inside active baseline bounds." }
                }),
            };
            stdout.write_all(format!("{}\n", response.to_string()).as_bytes()).await?;
            stdout.flush().await?;
        }
    }
    Ok(())
}
