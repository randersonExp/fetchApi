# Project Overview 
This project is a FastAPI implementation of the challenge posted [here](https://github.com/fetch-rewards/receipt-processor-challenge). FastAPI is something I've enjoyed using recently since it supplies the simple syntax of Python, while having performance and scalability in the same ballpark as Node and Go for I/O bound APIs. Since Python is the premier language for ML/DS solutions, this also makes it an ideal candidate when developing APIs and tooling alongside machine learning engineers! 

# Running the Project via Docker Container (Optional)
Note: You should be able to run and test via the Docker container. 
1. Make sure you are at the root level of the `fetchApi` repository, since that is where our Dockerfile exists!
2. Build the image locally and give it the tag `fetchapi` like so:
```
docker build -t fetchapi .
```

3. Run the container and turn on port forwarding. For testing, I used port 8000 like so:
```
docker run -d -p 8000:80 fetchapi
```

4. At this point, you should have a running container and you should be able to get a successful liveliness check by 
navigating to the following in your web browser: `http://127.0.0.1:8000/`. It will print the following message to the screen:
```
{"message":"Liveliness check passed!!"}
```

# Local Development
1. Install Python 3.8.*. For this, 3.8.12 is recommended. Link: https://www.python.org/downloads/.
2. For good practice's sake, we should create a virtual env to create an isolated environment for our FastAPI project. Run:
```
$ python3 -m venv env
```
In order to use the environment’s packages/resources in isolation, you need to “activate” it. To do this, just run the following:
```
source env/bin/activate
```
3. Within the root folder, run:
```
pip install -r api/requirements.txt
```
4. Run the FastAPI web server with the following command: `uvicorn api.main:createApp --reload`
5. To test it, the directions are the same as they were when building via the Docker image! A liveliness check is exposed and can be accessed at the following URL: `http://127.0.0.1:8000/`



