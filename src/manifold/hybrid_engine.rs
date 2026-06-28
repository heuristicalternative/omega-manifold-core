//! Hybrid Telemetry and Dimensional Coordinate Mapping Subsystem
//! Tracks runtime optimization metrics and structural drift across execution blocks.

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct ManifoldCoordinate {
    pub dimension: u32,
    pub trajectory: f64,
    pub displacement: f64,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct OptimizationTrace {
    pub anchor_hex: u8,
    pub coordinate: ManifoldCoordinate,
    pub token_efficiency: f64,
    pub latency_ms: f64,
    pub drift_coefficient: f64,
}
