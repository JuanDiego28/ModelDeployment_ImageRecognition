#  Image Classification Model deployment, Flask ML API

## The Business problem

Imagine that you work for a company that has a large collection of images and needs to automatically classify them into different categories. This task can be time-consuming and error-prone when done manually by human workers.

## Project Overview

### Objective:
We aim to develop a robust solution employing a Convolutional Neural Network (CNN) implemented in Tensorflow. This sophisticated approach enables us to automate the image classification process, achieving high accuracy and efficiency.

### System Components
* Web User Interface (UI):

Allows users to effortlessly upload images.
Facilitates the retrieval of predicted image classes.

* Python Flask API:

Serves as the backend for the CNN implementation.
Receives uploaded images, preprocesses them (e.g., resize, normalize), and interfaces with the CNN.
Returns the predicted class in JSON format.
Handles errors gracefully, providing informative messages to the UI in case of any issues.

* Message broker:

We used Redis to stablish a comunication between the components of our system

* Machine learning model:

TensorFlow CNN:While we won't delve into the intricacies of building a TensorFlow CNN from scratch, we assure you that we have a robust solution in place. We'll leverage a pre-trained model for this project to streamline the process.


## Technical aspects

The technologies involved are:
- Python is the main programming language
- Flask framework for the API
- HTML for the web UI
- Redis for the communication between microservices
- Tensorflow for loading the pre-trained CNN model
- Locust for doing the stress testing of the solution

