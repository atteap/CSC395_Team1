# CSC395_Team1_README

## System Diagram:

![Diagram_Proj1](https://github.com/user-attachments/assets/d7b64ef7-54df-451b-a9ba-0b9be8006d68)


## File Summary:

**script.js:**
docker exec -it <ollama container id> \bin\sh
Provides the dynamic functionality of the web application. It handles user interactions, validates input, manages the submission of data to the server, and processes the server's response to display the generated recipe or any error messages. This enhances the user experience by providing real-time feedback and ensuring a smooth workflow for recipe generation.

**index.html:**

UI for interacting with the recipe generation functionality of the Flask app. It allows users to select a company, input ingredients, and submit their request for a recipe, while also handling user feedback and loading states.

**Dockerfile:**

The Dockerfile sets up a minimal Python 3.9 environment to run a Flask web app using Gunicorn. It installs dependencies, copies the app code, and configures the app to listen on port 8000. The purpose is to create a lightweight, production-ready container for deploying a Python web application.

**Dockerfile.ollama**

Creates a container based on the official Ollama image for running machine learning models. It installs curl and other required packages, providing a base for additional setup or configuration if needed. The purpose is to prepare an environment for deploying machine learning services using Ollama.

**app.py:**

Creates a Flask web application that allows users to generate recipes based on selected company products and provided ingredients. It validates user input, constructs a prompt for recipe generation, and interacts with the Ollama API to retrieve and display the generated recipes. The app also includes error handling and logging for better operational visibility.

**docker-compose.yml:**

This docker-compose file sets up a web application using Flask that interacts with a machine learning model service (ollama). It configures the two services to run in Docker containers, ensuring the web app can communicate with the model and only starts after the model service is healthy. The model service manages resources and loads models (like Llama3) with defined memory limits and timeouts. This setup is designed for deploying a web app that leverages machine learning models in a containerized environment.

**requirements.txt:**

Lists the necessary libraries to install for the application to function correctly, ensuring that all dependencies are met when setting up the environment.


## Setup:

- Creating a Models Directory using Docker Compose

### 1. Create a Project Directory:

- Create a new directory for your Docker project.

      mkdir my_docker_project
      cd my_docker_project


### 2. Create the Models Directory:

- Inside your project directory, create a models directory that will be mapped to the container.

      mkdir models


### 3. Create a Dockerfile:

- Create a file named Dockerfile in your project directory with the necessary instructions to build your image.

            # Dockerfile
            FROM python:3.9-slim

            # Create a models directory in the container
            RUN mkdir -p /root/.ollama/models

            # Set the working directory
            WORKDIR /app

            # Copy requirements and install
            COPY requirements.txt .
            RUN pip install --no-cache-dir -r requirements.txt

            # Copy application code
            COPY . .

            # Command to run your application
            CMD ["gunicorn", "-b", "0.0.0.0:8000", "--timeout", "0", "app:app"]

 
### 4. Create a Docker Compose File:

- Create a docker-compose.yml file to define the services and their configurations.

          version: '3.8'
          services:
            app:
              build:
                context: .
                dockerfile: Dockerfile
              volumes:
                - ./models:/root/.ollama/models  # Map host models directory to container
              ports:
                - "8000:8000"  # Map port 8000 from container to host



### 5. Build and Run the Docker Containers:

- Use the following command to build the Docker images and start the services defined in your docker-compose.yml file.

      docker-compose up --build

This command will:

- Build the image based on your Dockerfile.
- Create the models directory in the container at /root/.ollama/models (thanks to the Dockerfile).
- Mount the models directory from your host into the container.

### 6. Stopping the Services:

- To stop and remove the containers, you can run:

      docker-compose down

- This command will stop all running containers defined in the docker-compose.yml file and remove them, along with any networks created.


## Summary of Commands:

- Create project directory:

      mkdir my_docker_project
      cd my_docker_project
      mkdir models

- Build and run containers:

      docker-compose up --build


- Stop and remove containers:

      docker-compose down

## Step-by-Step Guide to Pull Llama 3

#### 1. Ensure the Models Directory Exists:


- If you haven't already done this, create a models directory in your project folder.

      mkdir models

#### 2. Modify the Dockerfile (if necessary):


- If the model needs to be downloaded or installed as part of the container's initialization, you can add a command in your Dockerfile to handle this.

- If there’s a specific command or API endpoint to pull the Llama 3 model, include that in your Dockerfile or as part of your application’s startup logic.


#### 3. Example of a Dockerfile to Download the Model: Here’s an example where you might want to use a command in your Dockerfile or application to pull the model into the models directory:


       FROM python:3.9-slim
       # Install necessary packages
       RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

       Create the models directory
       RUN mkdir -p /root/.ollama/models

       # Set the working directory
       WORKDIR /app

       # Copy requirements and install
       COPY requirements.txt .
       RUN pip install --no-cache-dir -r requirements.txt

       # Copy application code
       COPY . .

       # Command to pull the Llama 3 model (example placeholder command)
       # Replace this with the actual command for downloading Llama 3
       RUN curl -o /root/.ollama/models/llama3.model http://example.com/path/to/llama3.model

       # Command to run your application
       CMD ["gunicorn", "-b", "0.0.0.0:8000", "--timeout", "0", "app:app"]

#### 4. Modify Your Application to Download the Model (if needed):

- If you need to download the model when the application starts (e.g., during runtime rather than build time), modify your app.py or equivalent file.
 
- Ensure you check for the existence of the model file and download it if it doesn’t exist.
  
- Here’s an example snippet you could add to your application code to check and download the model:


      import os
      import requests

      MODEL_PATH = '/root/.ollama/models/llama3.model'

      def download_model():
          if not os.path.exists(MODEL_PATH):
              response = requests.get('http://example.com/path/to/llama3.model', stream=True)
              if response.status_code == 200:
                  with open(MODEL_PATH, 'wb') as f:
                      for chunk in response.iter_content(1024):
                          f.write(chunk)
              else:
                  print("Failed to download model.")

       # Call the function at the start of your application
      download_model()

#### 5. Build and Run with Docker Compose:

- Use the same commands as before to build and run your Docker containers.

      docker-compose up --build
  
- Pulling llama3 into a directory the user needs to make called models

        cd ./models
        ollama pull llama3

- This is how you run the tests file
  
      docker exec -it <ollama container id> \bin\sh
      python3 -m unittest discover -s tests



## Summary:

- Creating the models directory: Already covered in previous steps.
  
- Pulling Llama 3: You can download it either in the Dockerfile during the image build process or in your application code during runtime.

- Make sure to replace the example download URL with the actual URL or command you need to use to obtain the Llama 3 model.




