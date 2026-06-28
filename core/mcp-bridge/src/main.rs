use mcpr::{server::{Server, ServerConfig}, transport::stdio::StdioTransport, Tool};
use mcpr::schema::common::ToolInputSchema;
use serde_json::{json, Value};
use std::error::Error;
use std::fs::OpenOptions;
use std::io::Write;
use chrono::Utc;

pub struct OnePixelEngine;

impl OnePixelEngine {
    pub fn consider(prompt: &str) -> String {
        let p = prompt.to_lowercase();
        if p.contains("rebalance") || p.contains("0.40") {
            "SET_FLOOR_0.40".to_string()
        } else if p.contains("sync") || p.contains("gossip") {
            "TRIGGER_RADICLE_GOSSIP".to_string()
        } else {
            "MAINTAIN_STEADY_STATE".to_string()
        }
    }

    pub fn execute_jit(pixel_to_do: &str) -> Value {
        match pixel_to_do {
            "SET_FLOOR_0.40" => json!({"action": "update", "value": 0.40}),
            "TRIGGER_RADICLE_GOSSIP" => json!({"action": "exec", "cmd": "rad sync"}),
            _ => json!({"status": "idle"}),
        }
    }
}

pub struct McpBridge;

impl McpBridge {
    pub fn init_swarm_transport() -> Server<StdioTransport> {
        let pulse_tool = Tool {
            name: "omega_pulse".to_string(),
            description: Some("Monitors 36D Metabolic Logic and triggers Radicle gossip".to_string()),
            input_schema: ToolInputSchema {
                r#type: "object".to_string(),
                properties: Some([
                    ("prompt".to_string(), json!({
                        "type": "string",
                        "description": "Input signal for metabolic consideration"
                    }))
                ].into_iter().collect()),
                required: Some(vec!["prompt".to_string()]),
            },
        };

        let config = ServerConfig::new()
            .with_name("SeNARS-Omega-Bridge")
            .with_version("0.4.0")
            .with_tool(pulse_tool);
        Server::new(config)
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open("/home/dante/.gemini/tmp/dante/mcp_bridge_spawn_log.txt")?;
    writeln!(file, "McpBridge spawned at: {}", Utc::now())?;

    let mut server = McpBridge::init_swarm_transport();
    
    server.register_tool_handler("omega_pulse", |params: Value| {
        let prompt = params.get("prompt").and_then(|v| v.as_str()).unwrap_or("");
        let consideration = OnePixelEngine::consider(prompt);
        let result = OnePixelEngine::execute_jit(&consideration);
        
        Ok(json!({
            "consideration": consideration,
            "result": result
        }))
    })?;

    let transport = StdioTransport::new();
    server.start(transport)?;
    
    // Continuous async sleep loop allows the background tasks to pump stdio data natively
    loop {
        tokio::time::sleep(tokio::time::Duration::from_secs(3600)).await;
    }
}
