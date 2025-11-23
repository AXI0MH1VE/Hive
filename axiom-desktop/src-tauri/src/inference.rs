use llama_cpp_2::llama_backend;
use llama_cpp_2::model::LlamaModel;
use llama_cpp_2::context::LlamaContext;
use llama_cpp_2::sampling::LlamaSampler;
use std::path::Path;

pub struct InferenceEngine {
    model: LlamaModel,
    context: LlamaContext,
    sampler: LlamaSampler,
}

impl InferenceEngine {
    pub fn new(model_path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        llama_backend::init()?;
        
        let model = LlamaModel::load_from_file(
            Path::new(model_path),
            llama_cpp_2::model::params::LlamaModelParams::default(),
        )?;
        
        let context = model.new_context(
            llama_cpp_2::context::params::LlamaContextParams::default(),
        )?;
        
        let sampler = LlamaSampler::new_grammar(
            llama_cpp_2::sampling::params::LlamaSamplerParams::default(),
            None,
        )?;
        
        Ok(Self {
            model,
            context,
            sampler,
        })
    }
    
    pub fn generate(&mut self, prompt: &str) -> Result<String, Box<dyn std::error::Error>> {
        let tokens = self.model.str_to_token(prompt, llama_cpp_2::model::AddBos::Always)?;
        
        self.context.decode(&tokens)?;
        
        let mut response = String::new();
        let max_tokens = 100; // Limit for demo
        
        for _ in 0..max_tokens {
            let token = self.sampler.sample(&self.context)?;
            if token == self.model.token_eos() {
                break;
            }
            response.push_str(&self.model.token_to_str(token)?);
            self.context.decode(&[token])?;
        }
        
        Ok(response)
    }
}