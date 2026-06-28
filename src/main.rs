use omega_manifold_core::wal_23d::PreAllocatedWal23D;
use omega_manifold_core::manifold::OmegaManifoldEngine;
use omega_manifold_core::rhizome::RhizomeNode;
use omega_manifold_core::coordination::CoordinationEngine;
use std::error::Error;
use futures::StreamExt;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    tracing_subscriber::fmt::init();
    println!("Initializing UNIFIED HYPER-MANIFOLD OS Execution Core...");
    println!("Locked Baseline: {}", omega_manifold_core::G_UNIVERSAL_BASELINE);

    let mut wal = PreAllocatedWal23D::new();
    let manifold = OmegaManifoldEngine::new();
    let mut coordinator = CoordinationEngine::new();
    let mut p2p_node = RhizomeNode::new().await?;

    let test_coords = [0i64; 23];
    let test_values = [1.0, 5.0, 25.0];
    wal.append(test_coords, test_values, 1);

    loop {
        tokio::select! {
            event = p2p_node.swarm.select_next_some() => {
                tracing::debug!("Rhizome network event: {:?}", event);
            }
            _ = tokio::time::sleep(std::time::Duration::from_millis(100)) => {
                coordinator.monitor_thread_coherence(manifold.active_state);
            }
        }
    }
}
