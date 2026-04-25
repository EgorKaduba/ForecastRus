from openai import OpenAI

client = OpenAI(
    base_url="https://text.pollinations.ai/openai",
    api_key="anything"
)
def LLM_request(query: str) -> str:
    response = client.chat.completions.create(
        model="openai",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content