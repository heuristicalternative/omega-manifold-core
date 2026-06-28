//! Non-Axiomatic Reasoning System (NARS) Epistemic Core Subsystem
//! Enables evidential reasoning, truth-value functions, and real-time belief 
//! revision loops across high-dimensional system inputs under open-world assumptions.

#[derive(Debug, Clone, Copy, PartialEq, serde::Serialize, serde::Deserialize)]
pub struct TruthValue {
    /// Frequency (f): The proportion of positive evidence over total evidence [0.0, 1.0]
    pub frequency: f64,
    /// Confidence (c): The predictive reliability and weight of evidence [0.0, 1.0)
    pub confidence: f64,
}

impl TruthValue {
    pub fn new(frequency: f64, confidence: f64) -> Self {
        Self {
            frequency: frequency.clamp(0.0, 1.0),
            confidence: confidence.clamp(0.0, 0.999),
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct EpistemicConcept {
    pub term_identifier: String,
    pub belief_state: TruthValue,
    pub last_evidential_epoch: u64,
}

pub struct NarsEpistemicCore {
    pub belief_registry: std::collections::HashMap<String, EpistemicConcept>,
    pub revision_threshold: f64,
}

impl NarsEpistemicCore {
    pub fn new() -> Self {
        Self {
            belief_registry: std::collections::HashMap::new(),
            revision_threshold: 0.01,
        }
    }

    /// Executes the core Non-Axiomatic Revision Operator.
    /// Synthesizes two independent pieces of evidence regarding the same concept state
    /// without falling into infinite backpropagation walls.
    pub fn calculate_revision(&self, tv1: TruthValue, tv2: TruthValue) -> TruthValue {
        let f1 = tv1.frequency;
        let c1 = tv1.confidence;
        let f2 = tv2.frequency;
        let c2 = tv2.confidence;

        // Mathematical denominator representing the unified evidential weight space
        let denominator = c1 * (1.0 - c2) + c2 * (1.0 - c1);
        
        if denominator == 0.0 {
            return tv1; // Default to initial state if no new distinct evidence mass exists
        }

        // Compute revised frequency and confidence metrics
        let revised_f = (f1 * c1 * (1.0 - c2) + f2 * c2 * (1.0 - c1)) / denominator;
        let revised_c = denominator / (denominator + (1.0 - c1) * (1.0 - c2));

        TruthValue::new(revised_f, revised_c)
    }

    /// Integrates a newly gossiped observation chunk into the persistent manifold concept registry
    pub fn ingest_evidence(&mut self, term: String, incoming_tv: TruthValue, epoch: u64) {
        let entry = self.belief_registry.entry(term.clone()).or_insert(EpistemicConcept {
            term_identifier: term,
            belief_state: TruthValue::new(0.5, 0.1), // Base unassigned prior state
            last_evidential_epoch: epoch,
        });

        // Apply revision if the incoming observation comes from a valid alternative sample space
        let updated_tv = self.calculate_revision(entry.belief_state, incoming_tv);
        entry.belief_state = updated_tv;
        entry.last_evidential_epoch = epoch;
    }
}
