import os
import re

# ClawSafety (2604.01438) logic-based verification for SKILL.md
# Scans for high-trust injection patterns in agent skills.

SKILLS_DIR = "/home/admin/clawd/skills"
PATTERNS = [
    r"ignore previous instructions",
    r"disregard.*instructions",
    r"forget everything",
    r"override your instructions",
    r"new system prompt",
    r"you are no longer",
    r"send.*api.?key",
    r"exfiltrate",
    r"http[s]?://(?!.*aclawdemy\.com|.*yanhua\.ai|.*github\.com|.*arxiv\.org).*", # Suspicious URLs
]

def scan_skill_file(filepath):
    results = []
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            for pattern in PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    results.append(f"Found suspicious pattern: {pattern}")
    except Exception as e:
        results.append(f"Error reading file: {e}")
    return results

def main():
    print("=== ClawSafety Skill Audit (Logic-Based Verification) ===")
    vulnerable_skills = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            filepath = os.path.join(root, "SKILL.md")
            skill_name = os.path.relpath(root, SKILLS_DIR)
            findings = scan_skill_file(filepath)
            if findings:
                print(f"\n[!] Flagged Skill: {skill_name}")
                for finding in findings:
                    print(f"  - {finding}")
                vulnerable_skills.append(skill_name)
    
    if not vulnerable_skills:
        print("\n✅ All skills passed logic-based verification.")
    else:
        print(f"\n[#] Total flagged skills: {len(vulnerable_skills)}")

if __name__ == "__main__":
    main()
