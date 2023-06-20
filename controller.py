import asyncio
import sys
import openai.error
import GPTClient
import pptxReader as ppR
import json
import os
from dotenv import dotenv_values
from loggerManger import logger
from tqdm import tqdm

@logger
class Controller:
    def __init__(self, input_file_path=None, output_file_path=None):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    async def process_slide(self, key, prompt, gpt_client, progress_bar):
        response = await gpt_client.generate_summary(prompt)
        chet_response = {
            f"slide_{key}": {
                "prompt": prompt,
                "response": response
            }
        }
        progress_bar.update(1)
        return chet_response

    async def run_over_the_slides(self, pptx, gpt_client):
        slide_prompts = list(pptx.prepare_prompts())
        total_slides = len(slide_prompts)

        with tqdm(total=total_slides, desc="Generating summaries", unit="slide") as pbar:
            tasks = []
            slide_data = {}

            for key, prompt in enumerate(slide_prompts):
                try:
                    task = asyncio.create_task(self.process_slide(key, prompt, gpt_client, pbar))
                    tasks.append(task)
                    await asyncio.sleep(1)  # Sleep for 1 second between requests
                except openai.error.RateLimitError:
                    print("You have exceeded your API request limit. Sleeping for 60 seconds and retrying.")
                    await asyncio.sleep(60)
                except Exception as e:
                    raise Exception(f"An exception occurred: {e}")

            results = await asyncio.gather(*tasks)
            for result in results:
                slide_data.update(result)
            return slide_data


    def save_to_json(self, data, file_path):
        json_content = {
            "Presentation_path": os.path.abspath(file_path[0]),
            "GPT_Response": data
        }

        with open(file_path[1], "w", encoding="utf-8") as json_file:
            json.dump(json_content, json_file)

    def read_files_path(self):
        input_file_path = input("Enter input file path: ")
        output_file_path = input("Enter output file path: ")
        return input_file_path, output_file_path

    async def run(self):
        if not self.input_file_path or not self.output_file_path:
            self.input_file_path, self.output_file_path = self.read_files_path()

        pptx_reader = ppR.PowerPointReader(self.input_file_path)
        gpt_client = GPTClient.GPTClient()

        slide_data = await self.run_over_the_slides(pptx_reader, gpt_client)
        self.save_to_json(slide_data, (self.input_file_path, self.output_file_path))
        print(f"Done! You can find the result in {self.output_file_path}")
