import openai
import asyncio
from dotenv import dotenv_values
from typing import List
from tenacity import retry, wait_random_exponential, stop_after_attempt
import loggerManger
from tqdm import tqdm


class GPTClient:
    def __init__(self):
        """
        Initialize the GPTClient class
        set the question to ask the GPT-3.5 turbo model
        TODO: adding more question to ask the GPT-3.5 turbo model
        """
        openai.api_key = dotenv_values(".env")["OPENAI_API_KEY"]  # set the openai api key
        self.question = [
            "Summarize the following slide that I can understand it and learn from\
             it, give me the main points of the slide and examples if needed:"
        ]

    def generate_prompts(self, prompt: str):
        """
        Generate the prompt to send to the GPT-3.5 turbo model
        :param prompt: string to add to the question
        :return: chet GPT-3.5 turbo model prompt with the question and the prompt
        """
        formatted_prompts = f"{self.question[0]} \n {prompt}"
        return formatted_prompts

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(1))
    async def generate_summary(self, prompt, progress_bar=None):
        """
        Generate the summary from the GPT-3.5 turbo model
        :param prompt: the prompt to send to the GPT-3.5 turbo model
        :param progress_bar: progress bar to update (optional)
        :return: the summary from the GPT-3.5 turbo model
        """
        try:
            formatted_prompt = self.generate_prompts(prompt)
            chat_response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": formatted_prompt}
                ]
            )
            await asyncio.sleep(1)

            if progress_bar is not None:
                progress_bar.update(1)

            return chat_response["choices"][0]["message"]["content"]

        except openai.error as e:
            raise Exception(f"there problem with openai api: {e}")
        except Exception as e:
            raise Exception(f"There exception: {e}")


# test the GPTClient class
if __name__ == '__main__':
    gptClient = GPTClient()
    response = asyncio.run(gptClient.generate_summary("Explain me that is python language?"))
    print(response)
