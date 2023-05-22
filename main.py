import asyncio
import GPTClient
import pptxReader as ppR
import json


async def process_slide(prompt, gpt_client):
    reply = await gpt_client.generate_summary(prompt)
    return reply


async def process_slides(prompts: object, gpt_client: object) -> object:
    tasks = []
    for prompt in prompts:
        task = asyncio.create_task(process_slide(prompt, gpt_client))
        tasks.append(task)

    explanations = await asyncio.gather(*tasks)
    return explanations

def save_to_json(self, data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)


async def main():
    pptx_file_path = "/Users/dviravraham/Downloads/09-Spring-Listeners-Filters.pptx"
    output_file_path = "/Users/dviravraham/Downloads/explanations.json"
    api_key = "your_openai_api_key"

    powerpoint_reader = ppR.PowerPointReader(pptx_file_path)
    prompts = powerpoint_reader.prepare_prompts()

    gpt_client = GPTClient.GPTClient()
    explanations = await process_slides(prompts, gpt_client)

    save_to_json(explanations, output_file_path)


if __name__ == "__main__":
    asyncio.run(main())
