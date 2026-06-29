//! HEADER LAYER: L0 - Core Daemon Execution Frame
//! Bootstraps the primary workspace network loops and runtime environments safely.

use std::error::Error;
use omega_manifold_core::rhizome::bootstrap_rhizome_node;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Initialize global structured tracing logs
    tracing_subscriber::fmt::init();

    println!("--- Launching Omega Manifold Core Node ---");

    // Ignite the decentralized P2P transport network layer
    bootstrap_rhizome_node().await?;

    println!("RhizomeOS network loop active. Daemon engine running background peer listeners.");
    println!("Press Ctrl+C to terminate the runtime node frame safely.");

    // Keep the main thread alive while the network task processes frames in the background
    tokio::signal::ctrl_c().await?;
    println!("\nShutting down Omega Manifold Core Node gracefully.");
    
    Ok(())
}
