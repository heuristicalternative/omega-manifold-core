use core::sync::atomic::{AtomicUsize, Ordering};

pub const DIMENSIONS_23D: usize = 23;
pub const WAL_JOURNAL_MAX_23D: usize = 32;

#[derive(Debug, Clone, Copy, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum JournalStatus23D {
    CommitSuccess,
    FencedBoundaryViolation,
    SlotOverflow,
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct TransactionDelta23D {
    pub coordinates: [i64; DIMENSIONS_23D],
    pub value_vector: [f64; 3],
    pub epoch: u64,
}

pub struct PreAllocatedWal23D {
    pub journal: [Option<TransactionDelta23D>; WAL_JOURNAL_MAX_23D],
    pub write_ptr: AtomicUsize,
}

impl PreAllocatedWal23D {
    pub const fn new() -> Self {
        Self {
            journal: [None; WAL_JOURNAL_MAX_23D],
            write_ptr: AtomicUsize::new(0),
        }
    }

    pub fn append(&mut self, coordinates: [i64; DIMENSIONS_23D], values: [f64; 3], current_epoch: u64) -> JournalStatus23D {
        let current_idx = self.write_ptr.load(Ordering::Relaxed);
        
        if current_idx >= WAL_JOURNAL_MAX_23D {
            return JournalStatus23D::SlotOverflow;
        }

        let virtual_address = current_idx * core::mem::size_of::<TransactionDelta23D>();
        if (virtual_address & crate::MASTER_INVARIANT_MASK) != virtual_address {
            return JournalStatus23D::FencedBoundaryViolation;
        }

        let delta = TransactionDelta23D {
            coordinates,
            value_vector: values,
            epoch: current_epoch,
        };

        self.journal[current_idx] = Some(delta);
        self.write_ptr.fetch_add(1, Ordering::SeqCst);

        JournalStatus23D::CommitSuccess
    }
}
