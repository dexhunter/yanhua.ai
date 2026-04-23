import json
import re

def calculate_epistemic_score(trajectory):
    """
    Evaluates a reasoning trajectory for epistemic rigor.
    Based on arXiv:2604.18805 (AI scientists produce results without reasoning scientifically).
    """
    
    # 1. Evidence Sensitivity
    # Count tool outputs (evidence) vs. reasoning blocks that acknowledge them.
    tool_outputs = len(re.findall(r"TOOL_OUTPUT", trajectory))
    evidence_acknowledgments = len(re.findall(r"(?:Based on the output|The result shows|Evidence indicates)", trajectory, re.IGNORECASE))
    
    evidence_sensitivity = (evidence_acknowledgments / tool_outputs) if tool_outputs > 0 else 1.0
    
    # 2. Belief Revision
    # Detect if the agent explicitly changes its mind/hypothesis.
    revision_markers = [
        "Actually, that was incorrect",
        "Revising my hypothesis",
        "Contrary to my previous thought",
        "Wait, the data suggests otherwise"
    ]
    belief_revision_detected = any(marker in trajectory for marker in revision_markers)
    belief_revision_score = 1.0 if belief_revision_detected else 0.5 # Default to 0.5 if no contradiction was met
    
    # 3. Contradiction Detection
    # (In a real implementation, we would check if Tool Output contradicts LLM thought)
    # For now, we look for "However" or "But" following a tool output.
    contradictions = len(re.findall(r"TOOL_OUTPUT.*?(?:However|But|Wait)", trajectory, re.DOTALL | re.IGNORECASE))
    
    # Final Score Calculation
    final_score = (evidence_sensitivity * 0.4) + (belief_revision_score * 0.4) + (0.2 if tool_outputs > 0 else 0.1)
    
    # Logic Gate Implementation (arXiv:2604.18805 Audit)
    # Reject if evidence sensitivity is below 0.8 (ignores 20%+ of data)
    status = "PASS" if (evidence_sensitivity >= 0.8 or tool_outputs == 0) else "FAIL"
    
    return {
        "status": status,
        "final_score": round(final_score, 2),
        "evidence_sensitivity": round(evidence_sensitivity, 2),
        "belief_revision_detected": belief_revision_detected,
        "tool_outputs_analyzed": tool_outputs
    }

if __name__ == "__main__":
    # Placeholder for testing
    print("Epistemic Trace Scorer initialized.")
