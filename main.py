import os

from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError(
            "OPENROUTER_API_KEY environment variable was not found. "
            "Please set it in your environment or .env file."
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
            }
        ],
    )

    if response.usage is not None:
        print(
            f"Prompt tokens: {response.usage.prompt_tokens}\n"
            f"Response tokens: {response.usage.completion_tokens}"
        )
    else:
        raise RuntimeError("API response did not include usage information.")

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
