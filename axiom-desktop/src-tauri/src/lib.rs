mod audit_log;
mod inference;
mod vector_store;

use std::sync::Mutex;
use lazy_static::lazy_static;

lazy_static! {
    static ref INFERENCE_ENGINE: Mutex<Option<inference::InferenceEngine>> = Mutex::new(None);
    static ref VECTOR_STORE: Mutex<Option<vector_store::VectorStore>> = Mutex::new(None);
}

// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[tauri::command]
async fn initialize_engine(model_path: String) -> Result<String, String> {
    match inference::InferenceEngine::new(&model_path) {
        Ok(engine) => {
            *INFERENCE_ENGINE.lock().unwrap() = Some(engine);
            Ok("Engine initialized".to_string())
        }
        Err(e) => Err(format!("Failed to initialize engine: {}", e)),
    }
}

#[tauri::command]
async fn generate_response(prompt: String) -> Result<String, String> {
    let mut engine_guard = INFERENCE_ENGINE.lock().unwrap();
    if let Some(ref mut engine) = *engine_guard {
        match engine.generate(&prompt) {
            Ok(response) => Ok(response),
            Err(e) => Err(format!("Generation failed: {}", e)),
        }
    } else {
        Err("Engine not initialized".to_string())
    }
}

#[tauri::command]
async fn log_interaction(user_input: String, ai_response: String) -> Result<String, String> {
    Ok(audit_log::log_interaction(&user_input, &ai_response))
}

#[tauri::command]
async fn initialize_vector_store(db_path: String) -> Result<String, String> {
    match vector_store::VectorStore::new(&db_path) {
        Ok(store) => {
            *VECTOR_STORE.lock().unwrap() = Some(store);
            Ok("Vector store initialized".to_string())
        }
        Err(e) => Err(format!("Failed to initialize vector store: {}", e)),
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            greet,
            initialize_engine,
            generate_response,
            log_interaction,
            initialize_vector_store
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
