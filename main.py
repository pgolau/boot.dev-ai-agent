import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions
from prompts import system_prompt


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY environment variable was not found. "
            "Please set it in your environment or .env file."
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    generate_content(client, messages, args.user_prompt, args.verbose)


def generate_content(
    client: OpenAI,
    messages: list,
    user_prompt: str,
    verbose: bool,
) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,  # pyright: ignore[reportArgumentType]
        temperature=0,
    )
    if not response.usage:
        raise RuntimeError("API response did not include usage information.")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")  # pyright: ignore[reportAttributeAccessIssue]
            print(f"Calling function: {tool_call.function.name}({function_args})")  # pyright: ignore[reportAttributeAccessIssue]
    else:
        print(message.content)


if __name__ == "__main__":
    main()
