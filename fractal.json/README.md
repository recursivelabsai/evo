# Fractal.json Schemas

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
