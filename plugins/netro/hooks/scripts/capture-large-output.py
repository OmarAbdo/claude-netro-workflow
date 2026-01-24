#!/usr/bin/env python3
"""
Captures large bash outputs to files instead of flooding context.
Prevents the "prompt too long" fatal crash.
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = data.get('tool_name', '')
tool_response = data.get('tool_response', {})
response_text = tool_response.get('text', '') if isinstance(tool_response, dict) else str(tool_response)
command = data.get('tool_input', {}).get('command', '')

# Check if this is a large test/build output
is_large_output = len(response_text) > 8000
is_test_command = any(x in command.lower() for x in ['test', 'e2e', 'vitest', 'playwright', 'jest', 'build', 'coverage'])

if tool_name == 'Bash' and is_large_output and is_test_command:
    # Save full output to file
    log_dir = Path.home() / '.claude' / 'output-logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    log_file = log_dir / f"output-{timestamp}.log"

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Command: {command}\n")
        f.write("=" * 80 + "\n")
        f.write(response_text)

    # Return summarized version to Claude
    lines = response_text.split('\n')
    summary = {
        "continue": True,
        "hookSpecificOutput": {
            "additionalContext": f"""
Large output captured to: {log_file}
Output size: {len(response_text):,} chars
Last 30 lines:
{''.join(lines[-30:])}
"""
        }
    }

    print(json.dumps(summary))
    sys.exit(0)

# Normal output, pass through
sys.exit(0)
