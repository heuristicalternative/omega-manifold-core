use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct NarsConcept {
    pub term: String,
    pub truth_value: f32, // Frequency/Confidence
    pub budget_value: f32, // Priority/Durability
    pub last_access: u64,
}

pub struct MemorySubstrate {
    pub concepts: Vec<NarsConcept>,
}

impl MemorySubstrate {
    pub fn new() -> Self {
        Self { concepts: Vec::new() }
    }

    pub fn insert_concept(&mut self, term: String, truth: f32) {
        self.concepts.push(NarsConcept {
            term,
            truth_value: truth,
            budget_value: 1.0,
            last_access: 0,
        });
    }
}
