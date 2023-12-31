import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image


# Connect to Redis and assign to variable `db``
# Bring Redis settings like host, port, db. from settings.py module 
db = redis.Redis(host = settings.REDIS_IP, port = settings.REDIS_PORT, db= settings.REDIS_DB_ID, decode_responses= True)

# Load ML model and assign to variable `model`
model = ResNet50(include_top=True, weights="imagenet")

def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    class_name = None
    pred_probability = None

    # load image
    img_path = os.path.join(settings.UPLOAD_FOLDER,image_name)
    img = image.load_img(img_path, target_size=(224, 224))

    # preprocess image
    x = image.img_to_array(img)
    x_batch = np.expand_dims(x,axis= 0)
    x_batch = preprocess_input(x_batch)

    # make the prediction
    result = model.predict(x_batch)
    prediction = decode_predictions(result, top= 1)

    class_name = prediction[0][0][1]
    pred_probability = prediction[0][0][2]
    pred_probability = round(pred_probability,4)

    return class_name, pred_probability


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        # Take a new job from Redis
        _, msg = db.brpop(str(settings.REDIS_QUEUE))
        
        #convert msg to dictionary
        msg = json.loads(msg) 

        # Run your ML model on the given data
        class_name, pred_probability = predict(msg['image_name'])
        
        # Store model prediction in a dictionary:

        results = {
            "prediction": class_name,
            "score": float(pred_probability)
        }        
        # Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job sent
        db.set(msg['id'],json.dumps(results)) #json 

        # Sleep for a bit
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()
