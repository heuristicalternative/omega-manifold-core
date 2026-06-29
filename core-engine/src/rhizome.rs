//! Asynchronous P2P Rhizome Network Subsystem
//! Configures libp2p Swarm transport parameters under type-safe execution wrappers.

use libp2p::{gossipsub, mdns, noise, tcp, yamux, Swarm, SwarmBuilder};
use std::error::Error;
use std::time::Duration;
use libp2p::identity;
use tokio::sync::mpsc;

#[derive(libp2p::swarm::NetworkBehaviour)]
pub struct RhizomeBehaviour {
    pub gossipsub: gossipsub::Behaviour,
    pub mdns: mdns::tokio::Behaviour,
}

pub struct RhizomeNode {
    pub swarm: Swarm<RhizomeBehaviour>,
}

impl RhizomeNode {
    pub async fn new(_memento_tx: mpsc::Sender<Vec<u8>>) -> Result<Self, Box<dyn Error>> {
        let _id_keys = identity::Keypair::generate_ed25519();

        // Construct the modern multi-phase swarm transport pipeline
        let swarm = SwarmBuilder::with_new_identity()
            .with_tokio()
            .with_tcp(
                tcp::Config::default(),
                noise::Config::new,
                yamux::Config::default,
            )?
            .with_behaviour(|key| {
                let message_authenticity = gossipsub::MessageAuthenticity::Signed(key.clone());
                
                let gossipsub_config = gossipsub::ConfigBuilder::default()
                    .heartbeat_interval(Duration::from_millis(250))
                    .validation_mode(gossipsub::ValidationMode::Strict)
                    .build()
                    .expect("Valid structural gossipsub configuration expected");
                
                let gossipsub = gossipsub::Behaviour::new(message_authenticity, gossipsub_config)
                    .expect("Failed to initialize sovereign Gossipsub behavior");
                    
                let mdns = mdns::tokio::Behaviour::new(
                    mdns::Config::default(), 
                    key.public().to_peer_id()
                ).expect("Failed to initialize local mDNS network listener");
                
                RhizomeBehaviour { gossipsub, mdns }
            })?
            .with_swarm_config(|c| c.with_idle_connection_timeout(Duration::from_secs(60)))
            .build();

        Ok(Self { swarm })
    }
}
