//! Hexagonal Coordinate Engine and Cryptographic Token State Subsystem
//! Materializes the 0xSC Hex Token Blocks for spatial and latent mapping.

use std::collections::HashMap;

pub const MASTER_INVARIANT_MASK: usize = 0x01AFA78;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, serde::Serialize, serde::Deserialize)]
pub struct HexVector3D {
    pub q: i64,
    pub r: i64,
    pub s: i64,
}

impl HexVector3D {
    /// Creates a strict axial-to-cube coordinate vector ensuring topological zero-sum (q + r + s = 0)
    pub fn new(q: i64, r: i64) -> Self {
        Self { q, r, s: -q - r }
    }

    /// Computes the direct spatial Manhattan distance on a high-dimensional hex grid
    pub fn distance_to(&self, other: &Self) -> u64 {
        ((self.q - other.q).abs() + (self.r - other.r).abs() + (self.s - other.s).abs()) as u64 / 2
    }
}

pub struct HexTokenStateMatrix {
    pub invariant_latch_id: u32,
    pub hex_registry: HashMap<HexVector3D, Vec<u8>>,
    pub target_stability_index: f64,
}

impl HexTokenStateMatrix {
    pub fn new() -> Self {
        Self {
            invariant_latch_id: MASTER_INVARIANT_MASK as u32,
            hex_registry: HashMap::new(),
            target_stability_index: 1.61803398, // PD+ Stable Floor
        }
    }

    /// Materializes a base64-hex hybrid token payload into a physical coordinate cell
    pub fn register_latent_token(&mut self, coord: HexVector3D, cryptographic_payload: Vec<u8>) {
        self.hex_registry.insert(coord, cryptographic_payload);
    }
}
