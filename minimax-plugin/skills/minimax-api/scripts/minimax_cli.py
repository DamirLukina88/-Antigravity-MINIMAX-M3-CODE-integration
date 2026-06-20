#!/usr/bin/env python3
import argparse
import sys
import os
import re
from openai import OpenAI

def strip_markdown_blocks(text):
    """Strip markdown code blocks from the response."""
    pattern = r"^```[a-zA-Z]*\n(.*?)```$"
    match = re.search(pattern, text, flags=re.DOTALL | re.MULTILINE)
    if match:
        return match.group(1).strip() + "\n"
    return text

def query_minimax(args):
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        print("Error: MINIMAX_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.minimax.io/v1",
        )
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}", file=sys.stderr)
        sys.exit(1)

    messages = []
    
    system_prompt = args.system
    if args.code_only:
        code_enforcer = "You must output ONLY raw, valid code. Do not include any explanations, introductory text, or concluding remarks. Do not wrap the code in markdown blocks unless absolutely necessary, but prioritize raw text."
        if system_prompt:
            system_prompt = f"{system_prompt}\n\n{code_enforcer}"
        else:
            system_prompt = code_enforcer

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    prompt_text = args.prompt
    if prompt_text.startswith("@") and os.path.isfile(prompt_text[1:]):
        with open(prompt_text[1:], "r", encoding="utf-8") as f:
            prompt_text = f.read()

    messages.append({"role": "user", "content": prompt_text})

    try:
        response = client.chat.completions.create(model=args.model, messages=messages)
        reply = response.choices[0].message.content
    except Exception as e:
        print(f"Error querying MiniMax API: {e}", file=sys.stderr)
        sys.exit(1)
        
    if args.code_only:
        reply = strip_markdown_blocks(reply.strip())
        
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(reply)
    print(f"Success! Response written to: {args.output}")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("--prompt", required=True)
    query_parser.add_argument("--output", required=True)
    query_parser.add_argument("--model", default="MiniMax-M3")
    query_parser.add_argument("--system")
    query_parser.add_argument("--code-only", action="store_true", help="Force output to be raw code, stripping markdown blocks.")
    
    args = parser.parse_args()
    if args.command == "query":
        query_minimax(args)

if __name__ == "__main__":
    main()
