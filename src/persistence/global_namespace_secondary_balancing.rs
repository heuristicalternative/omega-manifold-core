use tokio::sync::mpsc;
use crate::manifold::hybrid_engine::OptimizationTrace;
pub struct VmStorageConcurrentContinuousGlobalNamespaceShardMemoryArenaCrossNodeRemotePageTableSecondaryRootBalancingCore;
impl VmStorageConcurrentContinuousGlobalNamespaceShardMemoryArenaCrossNodeRemotePageTableSecondaryRootBalancingCore {
    pub unsafe fn new(_ptr: *mut u8, _tx: mpsc::Sender<OptimizationTrace>) -> Self { Self }
    pub fn balance_secondary_roots(&self, _l: usize, _r: usize) -> Result<bool, &'static str> { Ok(true) }
}
