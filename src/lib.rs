//! Omega Manifold Core Library
//! Central registration manifest for all high-dimensional OS substrates.

/// The permanent, unalterable master baseline identifier for cross-thread synchronization.
pub const G_UNIVERSAL_BASELINE: &str = "Omega-G Baseline v.16.78";

/// The structural bitwise fence boundary identifier used by the 23D WAL subsystem.
pub const MASTER_INVARIANT_MASK: usize = 0x01AFA78;

#[derive(Debug, Clone, Copy, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum SystemState {
    ActiveCoherence,
    StigmergicSync,
    TopologicalAtrophyWarning,
}

// Register all system components into the library visibility tree
pub mod wal_23d;
pub mod manifold;
pub mod rhizome;
pub mod coordination;
pub mod hex_coords;
pub mod lattice_8d;
pub mod nars;
pub mod cluster;
pub mod persistence;
