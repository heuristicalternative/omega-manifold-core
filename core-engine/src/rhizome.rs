use libp2p::{gossipsub, mdns, noise, tcp, yamux, Swarm, SwarmBuilder};
use std::error::Error;
use std::time::Duration;
use libp2p::core::PeerId;
use libp2p::identity;

#[derive(libp2p::swarm::NetworkBehaviour)]
pub struct RhizomeBehaviour {
    pub gossipsub: gossipsub::Behaviour,
    pub mdns: mdns::tokio::Behaviour,
}

pub struct RhizomeNode {
    pub swarm: Swarm<RhizomeBehaviour>,
}

impl RhizomeNode {
    pub async fn new() -> Result<Self, Box<dyn Error>> {
        let local_key = identity::Keypair::generate_ed25519();
        let local_peer_id = PeerId::from(local_key.public());

        let mut swarm = SwarmBuilder::with_new_identity()
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
                    .build()?;
                
                let gossipsub = gossipsub::Behaviour::new(message_authenticity, gossipsub_config)?;
                let mdns = mdns::tokio::Behaviour::new(mdns::Config::default(), key.public().to_peer_id())?;
                
                Ok(RhizomeBehaviour { gossipsub, mdns })
            })?
            .with_swarm_config(|c| c.with_idle_connection_timeout(Duration::from_secs(60)))
            .build();

        let topic = gossipsub::IdentTopic::new("coord://manifold/36D/sync");
        swarm.behaviour_mut().gossipsub.subscribe(&topic)?;

        Ok(Self { swarm })
    }
}
