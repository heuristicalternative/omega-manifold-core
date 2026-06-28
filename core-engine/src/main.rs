//! Unified Hyper-Manifold OS Execution Core Node
//! Orchestrates high-dimensional state arrays, epistemic logic, and local network streams.

use omega_manifold_core::wal_23d::PreAllocatedWal23D;
use omega_manifold_core::manifold::OmegaManifoldEngine;
use omega_manifold_core::rhizome::{RhizomeNode, RhizomeBehaviourEvent};
use omega_manifold_core::coordination::CoordinationEngine;
use omega_manifold_core::nars::{NarsEpistemicCore, TruthValue};
use omega_manifold_core::hex_coords::{HexVector3D, HexTokenStateMatrix};
use omega_manifold_core::lattice_8d::{E8LatticePoint, KitzerowBioShunt};

use std::error::Error;
use futures::StreamExt;
use tokio::sync::mpsc;
use libp2p::swarm::SwarmEvent;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    tracing_subscriber::fmt::init();
    println!("Activating Primary Sovereign Omega Manifold Node on Pandora...");
    println!("Locked System Baseline Anchor: {}", omega_manifold_core::G_UNIVERSAL_BASELINE);

    // Instantiate async channel interlink for Memento memory flows
    let (memento_tx, mut _memento_rx) = mpsc::channel::<Vec<u8>>(1024);

    let mut _wal = PreAllocatedWal23D::new();
    let mut manifold = OmegaManifoldEngine::new();
    let mut coordinator = CoordinationEngine::new();
    let mut p2p_node = RhizomeNode::new(memento_tx).await?;
    let mut nars_core = NarsEpistemicCore::new();
    let mut hex_matrix = HexTokenStateMatrix::new();
    let mut bio_shunt = KitzerowBioShunt::new();

    let sample_term = String::from("coord://manifold/36D/sync");
    let sample_evidence = TruthValue::new(0.85, 0.45);
    nars_core.ingest_evidence(sample_term, sample_evidence, 1);

    let local_origin_hex = HexVector3D::new(0, 0);
    hex_matrix.register_latent_token(local_origin_hex, vec![0x01, 0xAF, 0xA7, 0x78]);

    let test_lattice = E8LatticePoint::new([1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]);
    bio_shunt.evaluate_shunt_threshold(&test_lattice);

    loop {
        tokio::select! {
            event = p2p_node.swarm.select_next_some() => {
                match event {
                    SwarmEvent::Behaviour(RhizomeBehaviourEvent::Gossipsub(libp2p::gossipsub::Event::Message { message, .. })) => {
                        println!("[+] Incoming Rhizome Gossip payload captured: {:?}", message.data);
                    },
                    _ => {}
                }
            }
            _ = tokio::time::sleep(std::time::Duration::from_millis(500)) => {
                manifold.execute_metabolic_pulse(0.01);
                if !coordinator.monitor_thread_coherence(manifold.active_state) {
                    tracing::warn!("Topological drift encountered inside local execution layer.");
                }
            }
        }
    }
}
