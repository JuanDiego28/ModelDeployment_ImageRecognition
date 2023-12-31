import json
import time
from uuid import uuid4

import redis
# import settings
import settings

# Connect to Redis and assign to variable `db``
# Bring Redis settings: host, port, db. from settings.py module
db = redis.Redis(host = settings.REDIS_IP, port = settings.REDIS_PORT, db= settings.REDIS_DB_ID, decode_responses= True)


def model_predict(image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    prediction = None
    score = None
    
    # Assign an unique ID for this job and add it to the queue.
    # to keep track of this particular job across all the services
    job_id = str(uuid4())

    # Create a dict with the job data we will send through Redis 
    job_data = {
        "id": job_id,
        "image_name": image_name
    }
    
    # Send the job to the model service using Redis
    db.lpush(settings.REDIS_QUEUE,json.dumps(job_data))
    
    #tracking if redis connection is ok
    try: print("db.ping = ", db.ping())
    except Exception: print('error with redis')

    # Loop until we received the response from our ML model
    while True:
        # Attempt to get model predictions using job_id
        output = db.get(job_id)

        # Check if the text was correctly processed by our ML model
        if output is not None:
            # output = json.loads(output.decode("utf-8"))
            output = json.loads(output)
            prediction = output["prediction"]
            score = output["score"]

            db.delete(job_id)
            break

        # Sleep some time waiting for model results  
        time.sleep(settings.API_SLEEP)

    return prediction, score
