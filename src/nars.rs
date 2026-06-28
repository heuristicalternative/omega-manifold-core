#[derive(Debug, Clone, Copy, PartialEq, serde::Serialize, serde::Deserialize)]
pub struct TruthValue { pub frequency: f64, pub confidence: f64 }
impl TruthValue { pub fn new(f: f64, c: f64) -> Self { Self { frequency: f, confidence: c } } }
pub struct NarsEpistemicCore;
impl NarsEpistemicCore {
    pub fn new() -> Self { Self }
    pub fn ingest_evidence(&mut self, _term: String, _tv: TruthValue, _epoch: u64) {}
}
