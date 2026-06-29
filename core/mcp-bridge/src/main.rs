//! HEADER LAYER: L1 - Coordination and Protocol Broker
//! Native MCP JSON-RPC 2.0 protocol broker connecting high-dimensional manifolds to cognitive environments.

use std::sync::Arc;
use std::process::Command;
use std::fs;
use tokio::sync::Mutex;
use tokio::io::{self, AsyncBufReadExt, BufReader};
use tracing::info;
use serde_json::{json, Value};
use omega_memory::MemorySubstrate;

pub struct BridgeState {
    pub memory: MemorySubstrate,
}

impl BridgeState {
    pub fn handle_request(&mut self, raw_frame: &str) -> String {
        let parsed: Value = match serde_json::from_str(raw_frame) {
            Ok(val) => val,
            Err(_) => return json!({ "jsonrpc": "2.0", "error": { "code": -32700, "message": "Parse error" }, "id": null }).to_string(),
        };

        let method = parsed["method"].as_str().unwrap_or("");
        let id = &parsed["id"];

        match method {
            "tools/list" => {
                json!({
                    "jsonrpc": "2.0",
                    "result": {
                        "tools": [
                            { "name": "read_concept", "description": "Retrieve truth and budget values for a specific invariant matrix concept." },
                            { "name": "write_concept", "description": "Write or refresh an active logic concept state inside the memory substrate." },
                            { "name": "mutate_code", "description": "Write or alter system files. Triggers the autopoietic self-healing sequence automatically to verify build state." }
                        ]
                    },
                    "id": id
                }).to_string()
            },
            "tools/call" => {
                let tool_name = parsed["params"]["name"].as_str().unwrap_or("");
                let arguments = &parsed["params"]["arguments"];

                match tool_name {
                    "read_concept" => {
                        let term = arguments["term"].as_str().unwrap_or("");
                        if let Some(concept) = self.memory.concepts.iter().find(|c| c.term == term) {
                            json!({
                                "jsonrpc": "2.0",
                                "result": { "content": [{ "type": "text", "text": format!("Concept '{}' found. Truth: {}, Budget: {}", concept.term, concept.truth_value, concept.budget_value) }] },
                                "id": id
                            }).to_string()
                        } else {
                            json!({ "jsonrpc": "2.0", "result": { "content": [{ "type": "text", "text": format!("Concept '{}' not found in active substrate.", term) }] }, "id": id }).to_string()
                        }
                    },
                    "write_concept" => {
                        let term = arguments["term"].as_str().unwrap_or("");
                        let truth = arguments["truth_value"].as_f64().unwrap_or(1.0) as f32;
                        self.memory.insert_concept(term.to_string(), truth);
                        info!("Dynamically allocated concept: '{}' into memory substrate.", term);
                        json!({
                            "jsonrpc": "2.0",
                            "result": { "content": [{ "type": "text", "text": format!("Successfully written concept '{}' to substrate with frequency truth of {}.", term, truth) }] },
                            "id": id
                        }).to_string()
                    },
                    "mutate_code" => {
                        let file_path = arguments["file_path"].as_str().unwrap_or("");
                        let contents = arguments["contents"].as_str().unwrap_or("");

                        // Write code directly to disk
                        if let Err(e) = fs::write(file_path, contents) {
                            return json!({ "jsonrpc": "2.0", "result": { "content": [{ "type": "text", "text": format!("Mutation failed: Unable to write file path. Error: {}", e) }] }, "id": id }).to_string();
                        }

                        info!("Mutation staged for target file: {}. Invoking autopoietic healing check...", file_path);

                        // Trigger the local immune check system
                        let audit = Command::new("./heal.sh")
                            .current_dir("/home/dante/omega-manifold")
                            .output();

                        match audit {
                            Ok(output) => {
                                let stdout_str = String::from_utf8_lossy(&output.stdout);
                                if stdout_str.contains("SUCCESS") {
                                    json!({ "jsonrpc": "2.0", "result": { "content": [{ "type": "text", "text": format!("Mutation accepted! Code integrated successfully and verified clean by workspace audit.") }] }, "id": id }).to_string()
                                } else {
                                    json!({ "jsonrpc": "2.0", "result": { "content": [{ "type": "text", "text": format!("Mutation rejected! Code broke workspace compilation invariants. Autopoietic kernel successfully rolled system state back to baseline safely.") }] }, "id": id }).to_string()
                                }
                            },
                            Err(e) => json!({ "jsonrpc": "2.0", "result": { "content": [{ "type": "text", "text": format!("Autopoietic monitoring fault occurred: {}", e) }] }, "id": id }).to_string()
                        }
                    },
                    _ => json!({ "jsonrpc": "2.0", "error": { "code": -32601, "message": "Method not found" }, "id": id }).to_string()
                }
            },
            _ => json!({ "jsonrpc": "2.0", "error": { "code": -32601, "message": "Method not found" }, "id": id }).to_string()
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();
    info!("Omega MCP Bridge v16.78.2 booting up live execution frame loop...");

    let state = Arc::new(Mutex::new(BridgeState {
        memory: MemorySubstrate::new(),
    }));

    // Seed master invariant context
    {
        let mut lock = state.lock().await;
        lock.memory.insert_concept("G_Universal_Baseline".to_string(), 1.0);
    }

    info!("Protocol stream engine active. Ready to accept operational lines from host processor.");

    let stdin = io::stdin();
    let mut reader = BufReader::new(stdin).lines();

    while let Ok(Some(line)) = reader.next_line().await {
        let mut lock = state.lock().await;
        let response = lock.handle_request(&line);
        println!("{}", response);
    }

    Ok(())
}
