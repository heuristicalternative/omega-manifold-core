//! HEADER LAYER: L4 - Persistent State Engine (The Vault)
//! Provides serialized transactional logging of high-dimensional manifold transformations.

use std::fs::{OpenOptions, File};
use std::io::{Write, BufReader};
use std::path::Path;
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct VaultTransaction {
    pub timestamp: u64,
    pub dimension_count: u32,
    pub invariant_tag: String,
    pub synergetic_coherence: f32,
}

pub struct InvariantVault {
    pub storage_path: String,
}

impl InvariantVault {
    pub fn new(path: &str) -> Self {
        Self {
            storage_path: path.to_string(),
        }
    }

    pub fn commit_transaction(&self, tag: &str, dimensions: u32, coherence: f32) -> Result<(), Box<dyn std::error::Error>> {
        let log_file_path = Path::new(&self.storage_path);
        
        let mut transactions: Vec<VaultTransaction> = if log_file_path.exists() {
            let file = File::open(log_file_path)?;
            let reader = BufReader::new(file);
            serde_json::from_reader(reader).unwrap_or_else(|_| vec![])
        } else {
            vec![]
        };

        let tx = VaultTransaction {
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)?
                .as_secs(),
            dimension_count: dimensions,
            invariant_tag: tag.to_string(),
            synergetic_coherence: coherence,
        };

        transactions.push(tx);

        let mut file = File::create(log_file_path)?;
        let serialized = serde_json::to_string_pretty(&transactions)?;
        file.write_all(serialized.as_bytes())?;

        Ok(())
    }
}
