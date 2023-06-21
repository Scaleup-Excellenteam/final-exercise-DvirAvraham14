import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.environ.get('SERVER_HOST')
local = "/Users/dviravraham/PycharmProjects/final-exercise-DvirAvraham14/pres.pptx"
def send_request_with_file(file_path):
    with open(file_path, 'rb') as file:
        response = requests.post(BASE_URL + '/add', files={'upload_file': file})
        if response.status_code == 200:
            response_mess = response.json()
            return response_mess
        else:
            print("File upload failed. Status code:", response.status_code)
            return response.json()

def get_status_request(command: str):
    uuid = command.split()[1]
    response = requests.get(BASE_URL + '/get/' + uuid)
    if response.status_code == 200:
        response_mess = response.json()
        return response_mess
    else:
        print("File status request failed. Status code:", response.status_code)
        return response.json()


if __name__ == '__main__':
    while True:
        request = input("Enter the file path (or 'quit' to exit): ").strip()
        try:
            result = None
            if request == 'quit':
                break
            elif request.startswith('status'):
                result = get_status_request(request)
            else:
                result = send_request_with_file(request)
            if result:
                print(json.dumps(result, indent=4))
        except FileNotFoundError:
            print("File not found. Please enter a valid file path.")
        except IOError as e:
            print("Error occurred while reading the file:", str(e))
