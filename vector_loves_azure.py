#!/usr/bin/env python3

# Copyright (c) 2018 Hassan Habib

"""Tell Me What You See!

Make Vector describe what he sees using Azure Cognitive Services & Vector SDK
"""

import anki_vector
import requests
import random
import string
import os

def identify_image(image, image_id):
    headers = {'content-type' : 'application/octet-stream'}
    params  = {'visualFeatures': 'Description', 'subscription-key': 'YOUR_AZURE_SUBSCRIBTION_KEY_HERE'}
    filename = f"{image_id}.png"
    try:
        image.save(filename)
        fin = open(filename, 'rb')
        data = fin.read()
        response = requests.post('https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/analyze', headers=headers, params=params, data=data)
        seen = response.json()['description']['captions'][0]['text']
        print(seen)
        return "I see " + seen
    finally:
        fin.close()
        os.remove(filename)

def main():
    with anki_vector.Robot(enable_camera_feed=True) as robot:
        try:
                image = robot.camera.latest_image
                image_id = robot._camera._latest_image_id
                seen = identify_image(image, image_id)
                robot.say_text(seen)
        except:
                robot.say_text("I didn't get that, try again!")

if __name__ == "__main__":
    main()
