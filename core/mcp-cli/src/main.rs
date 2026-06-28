use clap::{Parser, Subcommand};
use serde_json::json;

#[derive(Parser)]
#[command(name = "omega-mcp-cli")]
struct Cli {
#[command(subcommand)]
command: Commands,
}

#[derive(Subcommand)]
enum Commands {
Ping,
}

#[tokio::main]
async fn main() {
let cli = Cli::parse();
match &cli.command {
    Commands::Ping => {
        let handshake = json!({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": { "clientInfo": { "name": "omega-shell-inspector", "version": "1.0.0" } }
        });
        println!("{}", handshake.to_string());
    }
}
}
