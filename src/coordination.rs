use crate::SystemState;
use std::time::{Duration, Instant};

pub struct CoordinationEngine {
    pub master_baseline: String,
    pub last_refresh: Instant,
    pub cycle_interval: Duration,
}

impl CoordinationEngine {
    pub fn new() -> Self {
        Self {
            master_baseline: String::from(crate::G_UNIVERSAL_BASELINE),
            last_refresh: Instant::now(),
            cycle_interval: Duration::from_millis(500),
        }
    }

    pub fn monitor_thread_coherence(&mut self, current_state: SystemState) -> bool {
        if self.last_refresh.elapsed() >= self.cycle_interval {
            self.last_refresh = Instant::now();
            match current_state {
                SystemState::ActiveCoherence | SystemState::StigmergicSync => return true,
                _ => return false,
            }
        }
        true
    }
}
