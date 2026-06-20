---
name: minimax-api
description: >-
  Query the MiniMax API for code generation and reasoning using MiniMax models (e.g., MiniMax-M3).
---

# MiniMax API Integration

## Overview
This skill provides a helper script that allows agents to programmatically query the MiniMax API. It uses the `MiniMax-M3` model by default. The API key and endpoint are configured in the script.

## Cost-Saving Workflows (MANDATORY)
When using MiniMax, you MUST optimize for token efficiency to save the user money:

1. **Direct-to-File Code Generation:** If you are asking MiniMax to write code or refactor a file, use the `--code-only` flag and specify the target project file as the `--output`. **DO NOT** read the resulting file back into your own context unless validation fails. MiniMax writes directly to the file!

## Utility Scripts
### `scripts/minimax_cli.py`

This is the primary script you must use to interact with MiniMax. 

**Arguments:**
- `--prompt` (required): The prompt or query you want to send to MiniMax. Use `@file.txt` to read from a file.
- `--output` (required): The file path where the MiniMax response should be written.
- `--model` (optional): Defaults to `MiniMax-M3`.
- `--system` (optional): An optional system prompt.
- `--code-only` (optional): **(CRITICAL)** Use this flag when generating code. It forces MiniMax to output ONLY code and strips all markdown formatting so the output file is instantly executable.

**Examples:**

Basic query:
```bash
python3 scripts/minimax_cli.py query --prompt "Explain the theory of relativity." --output /tmp/response.txt
```

Generating code directly to a file (Cost-Saving Workflow):
```bash
python3 scripts/minimax_cli.py query --code-only --prompt "Write a Python script to parse JSON." --output src/parser.py
```
