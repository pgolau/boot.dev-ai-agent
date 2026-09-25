import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


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
    )
    if not response.usage:
        raise RuntimeError("API response did not include usage information.")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
