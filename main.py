# import asyncio
# import sys
# import openai.error
# import GPTClient
# import pptxReader as ppR
# import json
# import os
# from dotenv import dotenv_values
# from loggerManger import logger
#
#
# @logger
# async def process_slide(key, prompt, gpt_client):
#     response = await gpt_client.generate_summary(prompt)
#     chet_response = {
#         f"slide_{key}": {
#             "prompt": prompt,
#             "response": response
#         }
#     }
#     return chet_response
#
#
# @logger
# async def run_over_the_slides(pptx, gpt_client) -> object:
#     tasks = []
#     slide_data = {}
#     for key, prompt in enumerate(pptx.prepare_prompts()):
#         try:
#             task = asyncio.create_task(process_slide(key, prompt, gpt_client))
#             tasks.append(task)
#             await asyncio.sleep(1)  # sleep for 1 second between requests
#         except openai.error.RateLimitError:
#             print(f"You over your api request limit going to sleep for 60 seconds and retry")
#             await asyncio.sleep(60)
#         except Exception as e:
#             raise Exception(f"There exception: {e}")
#
#     results = await asyncio.gather(*tasks)
#     for result in results:
#         slide_data.update(result)
#     return slide_data
#
# @logger
# def save_to_json(data, file_path: list) -> None:
#     """
#     Save the data to json file
#     :param data: the data to in json format
#     :param file_path: the file path to save the data
#     :return: nothing
#     """
#     json_content = {
#         "Presentation_path": os.path.abspath(file_path[0]),
#         "GPT_Response": data
#     }
#
#     with open(file_path[1], "w", encoding="utf-8") as json_file:
#         json.dump(json_content, json_file)
#
# @logger
# def read_files_path(*argv) -> list:
#     """
#     Read the files path from the user
#     :param argv: the files path
#     :return: list of the files path
#     """
#     files_path = list(argv)
#     if not files_path:
#         print("Please enter the input and output file path")
#         files_path.append(input("Enter input file path: "))
#         files_path.append(input("Enter output file path: "))
#     return files_path
#
# @logger
# async def main(*argv):
#     files_path = read_files_path(*argv)
#     pptx_reader = ppR.PowerPointReader(files_path[0])
#     gpt_client = GPTClient.GPTClient()
#
#     slide_data = await run_over_the_slides(pptx_reader, gpt_client)
#     save_to_json(slide_data, files_path)
#     print(f"Done, you can find the result in {files_path[1]}")
#
#
# if __name__ == "__main__":
#     asyncio.run(main(*sys.argv[1:]))
#     # asyncio.run(controller.main(*sys.argv[1:]))
import os.path
import sys
import asyncio
from controller import Controller


app = Controller(*sys.argv[1:])
asyncio.run(app.run())
