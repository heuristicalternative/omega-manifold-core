use std::collections::HashMap;
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, serde::Serialize, serde::Deserialize)]
pub struct HexVector3D { pub q: i64, pub r: i64, pub s: i64 }
impl HexVector3D { pub fn new(q: i64, r: i64) -> Self { Self { q, r, s: -q - r } } }
pub struct HexTokenStateMatrix { pub hex_registry: HashMap<HexVector3D, Vec<u8>> }
impl HexTokenStateMatrix {
    pub fn new() -> Self { Self { hex_registry: HashMap::new() } }
    pub fn register_latent_token(&mut self, coord: HexVector3D, payload: Vec<u8>) { self.hex_registry.insert(coord, payload); }
}
