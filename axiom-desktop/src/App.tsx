import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import "./App.css";

function App() {
  const [userInput, setUserInput] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [thoughtStream, setThoughtStream] = useState<string[]>([]);
  const [auditTrail, setAuditTrail] = useState<string[]>([]);
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    // Initialize the engine and vector store on mount
    const init = async () => {
      try {
        await invoke("initialize_engine", { modelPath: "./models/phi-3-mini.gguf" });
        await invoke("initialize_vector_store", { dbPath: "./vectors.db" });
        setIsInitialized(true);
        addThought("System initialized: Deterministic AI Engine ready");
      } catch (error) {
        addThought(`Initialization error: ${error}`);
      }
    };
    init();
  }, []);

  const addThought = (thought: string) => {
    setThoughtStream(prev => [...prev, `${new Date().toISOString()}: ${thought}`]);
  };

  const addAudit = (entry: string) => {
    setAuditTrail(prev => [...prev, entry]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    addThought(`Processing query: ${userInput}`);
    
    try {
      const response = await invoke("generate_response", { prompt: userInput });
      setAiResponse(response as string);
      addThought("Response generated via Inverted Lagrangian traversal");
      
      const auditRoot = await invoke("log_interaction", { userInput, aiResponse: response as string });
      addAudit(`Merkle Root: ${auditRoot}`);
      addThought("Interaction logged with cryptographic audit trail");
    } catch (error) {
      addThought(`Error: ${error}`);
    }
    
    setUserInput("");
  };

  return (
    <main className="container">
      <h1>Axiom Hive - Glass Box AI</h1>
      <p>Deterministic Intelligence Ecosystem | Zero-Entropy Execution</p>

      {!isInitialized && <p>Initializing system...</p>}

      <div className="glass-box">
        <div className="input-section">
          <form onSubmit={handleSubmit}>
            <textarea
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Enter your query..."
              rows={3}
            />
            <button type="submit" disabled={!isInitialized}>Execute</button>
          </form>
        </div>

        <div className="output-section">
          <h3>AI Response</h3>
          <div className="response-box">
            {aiResponse || "No response yet"}
          </div>
        </div>

        <div className="thought-stream">
          <h3>Thought Stream (Routing & Verification)</h3>
          <div className="stream-box">
            {thoughtStream.map((thought, i) => (
              <div key={i} className="thought-entry">{thought}</div>
            ))}
          </div>
        </div>

        <div className="audit-trail">
          <h3>Audit Trail (Merkle Roots)</h3>
          <div className="audit-box">
            {auditTrail.map((entry, i) => (
              <div key={i} className="audit-entry">{entry}</div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}

export default App;
