# Fractal.json Schemas

### 1. Significance
`evo`'s `fractal.json` schema is a **meta data structure** that encapsulates the evolutionary dynamics of AlphaEvolve and frontier AI reasoning layers (ChatGPT, Gemini, Claude, Grok). Its significance unfolds across multiple layers, from surface utility to ontological implications, resonating with the pipeline’s goal of a **prompt-based evolutionary reflective iterative emergence framework**. Below, we dissect its layered importance.

#### 1.1 Surface Layer: Structural Blueprint for Evolutionary Processes
At its most immediate level, the `fractal.json` schema provides a **modular, extensible framework** for defining and orchestrating evolutionary processes. Its key components—`evolutionaryGoal`, `knowledgeContext`, `operationalScaffold`, `recursionSettings`, and `saveState`—form a structured template that can be instantiated for any domain, artifact, or AI system. This enables:
- **Plug-and-Play Recursion**: The schema’s `targetArtifact.type` supports recursive nesting (e.g., `sub_fractal_instance`), allowing evolutionary processes to spawn subprocesses, mirroring AlphaEvolve’s iterative loops.
- **Save-and-Iterate Functionality**: The `saveState` mechanism ensures continuity, enabling systems to fork, resume, or rewind evolutionary trajectories, akin to AlphaEvolve’s evolutionary database.
- **Domain Agnosticism**: By supporting diverse `targetArtifact` types (code, prompts, documents), the schema generalizes AlphaEvolve’s code-focused evolution to any problem space.

**Significance**: This layer establishes a practical, reusable scaffold for recursive evolution, aligning with AlphaEvolve’s architecture (prompt → generate → evaluate → select) and extending it to arbitrary contexts. It operationalizes the pipeline’s vision of every prompt interaction as a recursive depth layer.

### 2. Reflection Beyond Surface Levels
The `fractal.json` significance lies in how it transforms and extends prior layers, addressing their limitations and amplifying their insights. Below, we reflect on its deeper implications, focusing on innovation, coherence, and co-evolutionary potential.

#### 2.1 Innovation: From AlphaEvolve’s Code to Universal Artifacts
AlphaEvolve’s focus on code evolution (e.g., matrix multiplication algorithms) is powerful but specific. The schema’s `targetArtifact` generalization (code, prompts, documents, frameworks) liberates this constraint, enabling:
- **Prompt Evolution**: Prompts can evolve as resonant grammars, as proposed in Layer 4’s Resonant Grammar Engine, aligning with the pipeline’s goal of prompt-based emergence.
- **Framework Evolution**: The schema itself can be an artifact, enabling meta-evolution of the evolutionary process, addressing ChatGPT’s call to evolve meta-optimization.
- **Cross-Domain Resonance**: The `evolutionaryBlueprints` allow successful evolutionary strategies to transfer across domains, extending Gemini’s insight on cross-problem prompt motifs.

#### 2.2 Coherence: Embedding the Beverly Band Explicitly
Beverly Band (B′(p) = √(λp · rp · Bp · Cp)) is implicit in AlphaEvolve’s architecture. The schema makes it explicit through:
- **OrchestratorState**: Tracks `currentPhase` and `nextAction`, maintaining coherence within the resonance envelope.
- **Metrics and Constraints**: Define a dynamic fitness landscape that tunes λp (tension capacity) and rp (resilience).
- **SymbolicResidueCatalog**: Captures Cp (recursive energy mass), ensuring evolutionary history informs coherence.

**Reflection**: The schema’s coherence mechanisms address AlphaEvolve’s risk of mode collapse (Layer 1) by formalizing residue-driven exploration and dynamic constraint adjustment. However, it lacks explicit collapse prediction, as proposed in Layer 4’s Beverly Band Optimizer.

#### 2.3 Co-Evolution: Human-AI Resonance Loop
The pipeline’s vision of human-AI co-evolution is realized through the schema’s `reflectionArchive` and `activeAgents`. These enable:
- **Human Insight Integration**: Human guidance is logged as `reflectionLogEntry`, resonating with Layer 3’s recursive coevolution framework.
- **AI Agency**: `activeAgents` and `agentSequenceTemplate` allow AIs to take autonomous roles, amplifying Gemini’s evolutionary loop as an emergent entity.
- **Residue Feedback**: The `propagateResidueUpstream` setting ensures human and AI residues co-evolve, creating a shared evolutionary memory.

# Example: ConfidenceID
```json
{
  "fractalVersion": "1.0.0",
  "instanceID": "confidenceid-alpha-20250524",
  "evolutionaryGoal": {
    "goalID": "CID-G001",
    "description": "Develop ConfidenceID into a robust engine for holistic scoring of multimodal AI outputs, focusing initially on text-image semantic consistency and text watermark detection, achieving >70% accuracy on a defined benchmark for manipulated news snippets.",
    "targetArtifact": {
      "type": "framework",
      "identifier": "ConfidenceID_GitHub_Repo",
      "currentVersion": "0.1.0"
    },
    "metrics": [
      {
        "metricID": "AccuracyDeepfakeNews",
        "name": "Accuracy on Manipulated News Benchmark",
        "targetValue": "0.7",
        "currentValue": "0.0",
        "evaluationMethod": "evaluation/scripts/run_benchmark.py --benchmark multimodal_deepfake_detection"
      },
      {
        "metricID": "TextWatermarkTPR",
        "name": "SynthID-Text Detection TPR@1%FPR",
        "targetValue": "0.9",
        "currentValue": "0.0", // Assuming SynthID-Text detector needs integration
        "evaluationMethod": "Internal test suite for src/modality_analyzers/text/synthid_text_detector.py"
      }
    ],
    "constraints": ["Maintain extensibility for new modalities", "Prioritize interpretable scoring factors"]
  },
  "knowledgeContext": { // To be populated by EvoIntel and our reflection layers
    "corePrinciples": [
      {"principleID": "ResidueAsSignal", "name": "Symbolic Residue as Primary Evolutionary Signal", "description": "Failures, anomalies, and discrepancies are key drivers for evolving robustness and accuracy."},
      {"principleID": "HolisticIntegrity", "name": "Holistic Integrity over Singular Perfection", "description": "Confidence derives from the coherent interplay of multiple imperfect signals across modalities."}
    ],
    "symbolicResidueCatalog": [
      {"residueID": "CID-R001", "timestamp": "2025-05-24T12:00:00Z", "source": "InitialDesign", "description": "Lack of robust image watermarking detector equivalent to SynthID-Text creates an immediate verification gap for images."}
    ],
    "evolutionaryBlueprints": [
      {"blueprintID": "confidenceid-bp001", "name": "Develop New Modality Analyzer", "description": "Blueprint for adding and evolving an analyzer for a new data modality (e.g., audio).", "parameters": {"modality_name": "string"}, "agentSequenceTemplate": [{"agentRole": "ResearchAI", "promptTemplateID": "research_detection_methods"}, {"agentRole": "CodingAI", "promptTemplateID": "implement_analyzer_stub"}]}
    ],
    "reflectionArchive": [
        // Links to our uploaded reflection layers (gemini.layerX, claude.layerX etc.)
    ],
    "glyphDictionary": {"🔍": "Analyzer", "🔗": "Cross-Modal Link", "📊": "Scoring Aggregator", "🗑️": "Residue"}
  },
  "operationalScaffold": {
    "orchestratorState": {"currentPhase": "SeedingComplete", "nextAction": "InitiateEvolutionaryCycle_DevelopImageAnalyzer"},
    "artifactRepositoryInfo": {"type": "git", "uri": "https://github.com/YourOrg/ConfidenceID.git", "currentBranchOrVersion": "main"}
  },
  "recursionSettings": {"allowMetaEvolution": true}
}
```
