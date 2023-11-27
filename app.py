from PIL import Image
import requests
import base64
import torch
from io import BytesIO
import numpy as np
import os
from json import loads, dumps

MANDATORY_ENV_VARS = ["API_URL", "API_TOKEN"]

for var in MANDATORY_ENV_VARS:
    if var not in os.environ:
        raise EnvironmentError(f"Failed to initialize because {var} is not set.")

API_URL = os.environ.get("API_URL")
headers = {
	"Authorization": f"Bearer {os.environ.get('API_TOKEN')}",
}

id2label = {
    "0": "Background",
    "1": "Hat",
    "2": "Hair",
    "3": "Sunglasses",
    "4": "Upper-clothes",
    "5": "Skirt",
    "6": "Pants",
    "7": "Dress",
    "8": "Belt",
    "9": "Left-shoe",
    "10": "Right-shoe",
    "11": "Face",
    "12": "Left-leg",
    "13": "Right-leg",
    "14": "Left-arm",
    "15": "Right-arm",
    "16": "Bag",
    "17": "Scarf"
  }

def handler(event, context):
    print("handler called")
    input = loads(event['body'])
    print("input loaded")
    response = requests.post(API_URL, headers=headers, json=input)
    print("response received")
    response_json = response.json()
    pred_seg = torch.tensor(response_json)
    pred_ids = pred_seg.unique()
    output = []
    for id in pred_ids:
        # print(f"processing id {id}")
        mask = (pred_seg == id)
        pil_image = Image.fromarray((mask * 255).numpy().astype(np.uint8))
        base64_string = image_to_base_64(pil_image)
        output.append({
            "score": 1,
            "label": id2label[str(id.item())],
            "mask": base64_string
        })

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": dumps(output)
    }

def image_to_base_64(image):
  buffered = BytesIO()
  image.save(buffered, format="PNG")
  img_str = base64.b64encode(buffered.getvalue())
  return img_str.decode('utf-8')
