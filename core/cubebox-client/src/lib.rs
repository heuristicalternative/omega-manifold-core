use tokio::sync::mpsc;
use tokio::time::{timeout, Duration};
use serde::{Serialize};
use std::error::Error;

pub struct CubeboxClient {
    pub tx: mpsc::Sender<String>,
}

impl CubeboxClient {
    pub async fn send_message<T: Serialize>(&self, message: T, timeout_ms: u64) -> Result<(), Box<dyn Error>> {
        // Serialize the message
        let serialized = serde_json::to_string(&message)?;

        // Send with Backpressure: 
        // This will 'await' if the channel is full
        let send_future = self.tx.send(serialized);

        // Apply timeout to prevent blocking
        match timeout(Duration::from_millis(timeout_ms), send_future).await {
            Ok(Ok(_)) => Ok(()),
            Ok(Err(e)) => Err(Box::new(e)),
            Err(_) => Err("Timeout: Message delivery failed".into()),
        }
    }
}
