import openai


class GPTClient:
    def __init__(self):
        openai.organization = "org-1rQWhdIGPx2e6WehVN7qX8QE"
        openai.api_key = "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"

    async def generate_summary(self, prompt):
        response = await openai.Completion.create(
            model="text-davinci-003",
            prompt="Create summarize for slide data for a student:\n\n slide data: " + prompt + "\n",
            temperature=0.7,
            max_tokens=64,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        reply = response.choices[0].text.strip()
        return reply


