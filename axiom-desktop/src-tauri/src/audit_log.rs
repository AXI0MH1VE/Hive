use rs_merkle::{MerkleTree, algorithms::Sha256};

// Placeholder for the Merkle Tree state (must be persisted)
static mut GLOBAL_TREE_LEAVES: Vec<[u8; 32]> = Vec::new();

pub fn log_interaction(user_input: &str, ai_response: &str) -> String {
    let data = format!("{}{}", user_input, ai_response);
    let hash = Sha256::hash(data.as_bytes());

    // UNSAFE block to modify static mutable state (for simplicity of blueprint)
    unsafe {
        GLOBAL_TREE_LEAVES.push(hash);
        let tree = MerkleTree::<Sha256>::from_leaves(&GLOBAL_TREE_LEAVES);
        // Return the new Root Hash as proof of state
        tree.root_hex().unwrap_or_else(|| "ERROR: Could not compute root".to_string())
    }
}

// Example usage:
// let root = log_interaction("Fix the bug", "Bug fixed with 9.18x efficiency.");
// print!("New Merkle Root: {}", root);