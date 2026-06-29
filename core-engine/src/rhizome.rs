//! HEADER LAYER: L3 - Decentralized Network Substrate (RhizomeOS)
//! Handles peer-to-peer discovery, transport binding, and secure frame inhalation over libp2p.

use std::error::Error;
use std::time::Duration;
use libp2p::{futures::StreamExt, identity, swarm::SwarmEvent, SwarmBuilder};
use tracing::info;

pub async fn bootstrap_rhizome_node() -> Result<(), Box<dyn Error>> {
    info!("RhizomeOS Network Substrate initializing...");

    // Generate local cryptographic identity keys
    let local_key = identity::Keypair::generate_ed25519();
    let local_peer_id = libp2p::PeerId::from(local_key.public());
    info!("Local cryptographic node identity instantiated: {}", local_peer_id);

    // Build the networking swarm using tokio defaults for TCP, Noise security, and Yamux multiplexing
    let mut swarm = SwarmBuilder::with_existing_identity(local_key)
        .with_tokio()
        .with_tcp(
            libp2p::tcp::Config::default(),
            libp2p::noise::Config::new,
            libp2p::yamux::Config::default,
        )?
        .with_behaviour(|_key| libp2p::swarm::dummy::Behaviour)?
        .with_swarm_config(|c| c.with_idle_connection_timeout(Duration::from_secs(30)))
        .build();

    // Bind to all local interfaces on an ephemeral, secure TCP port
    swarm.listen_on("/ip4/0.0.0.0/tcp/0".parse()?)?;

    info!("RhizomeOS network engine bound to socket. Awaiting data frames...");

    // Spawn the persistent network event inhalation loop
    tokio::spawn(async move {
        loop {
            match swarm.select_next_some().await {
                SwarmEvent::NewListenAddr { address, .. } => {
                    info!("RhizomeOS node actively listening on decentralized coordinate: {}", address);
                }
                SwarmEvent::IncomingConnection { local_addr, send_back_addr, .. } => {
                    info!("Secure connection vector initiated from {} to local receptor {}", send_back_addr, local_addr);
                }
                SwarmEvent::ConnectionEstablished { peer_id, endpoint, .. } => {
                    info!("Handshake successful. Connected to remote peer node: {} via {:?}", peer_id, endpoint);
                }
                SwarmEvent::ConnectionClosed { peer_id, cause, .. } => {
                    info!("Connection closed with peer node: {}. Reason: {:?}", peer_id, cause);
                }
                _ => {}
            }
        }
    });

    Ok(())
}
