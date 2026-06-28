use serde::{Deserialize, Serialize};
use serde_json::json;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};

#[derive(Debug, Serialize, Deserialize)]
struct JsonRpcRequest {
jsonrpc: String,
method: String,
#[serde(default)]
params: serde_json::Value,
id: serde_json::Value,
}

#[tokio::main]
async fn main() -> Result<(), Box> {
let stdin = tokio::io::stdin();
let mut stdout = tokio::io::stdout();
let mut reader = BufReader::new(stdin).lines();

while let Some(line) = reader.next_line().await? {
    if let Ok(req) = serde_json::from_str::(&line) {
        let response = match req.method.as_str() {
            "initialize" => json!({
                "jsonrpc": "2.0",
                "id": req.id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": { "name": "omega-mcp-bridge", "version": "16.78.2" }
                }
            }),
            _ => json!({
                "jsonrpc": "2.0",
                "id": req.id,
                "error": { "code": -32601, "message": "Method not found." }
            }),
        };
        stdout.write_all(format!("{}\n", response.to_string()).as_bytes()).await?;
        stdout.flush().await?;
    }
}
Ok(())
}
