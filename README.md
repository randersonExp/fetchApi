# Project Overview 
This project is a FastAPI implementation of the challenge posted [here](https://github.com/fetch-rewards/receipt-processor-challenge). FastAPI is something I've enjoyed using recently since it supplies the simple syntax of Python, while having performance and scalability in the same ballpark as Node and Go for I/O bound APIs. Since Python is the premier language for ML/DS solutions, this also makes it an ideal candidate when developing APIs and tooling alongside machine learning engineers! 

# Running the Project via Docker Container
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

Once the liveliness check passes, we are ready for some tests. I recommend a UI for calling this API, such as Postman. However, 
here are a few raw `curl` requests for those of us in a hurry. To post a receipt using the provided example: 
```
curl --location 'http://127.0.0.1:8000/receipts/process' \
--header 'Content-Type: application/json' \
--data '{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}'
```

To fetch points for a receipt with id `INSERT_ID_HERE`: 
```
curl --location 'http://127.0.0.1:8000/receipts/${INSERT_ID_HERE}/points'
```


# Local Development
This section describes how to continue developing this app on your local machine. 

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

# Running Unit Tests
Note: If you want to run tests, then read the 'Local Development' section first.
1. For testing the API routes:
```
python -m unittest api/tests/test_*.py
```

2. For testing our models:
```
python -m unittest models/tests/test_*.py
```

# Directory Structure
- Data models, (and business logic associated with them), are stored in the `models/` directory.
- API routes and all API logic is stored in the `api/` directory.
- Both directories have a `tests/` folder, which is where all unit test logic lives!


# TODOs
1. "Productionize" the Dockerfile better and build off of an Ubuntu base image.
2. Switch to a more robust package management solution instead of just a `requirements.txt` file. I typically use Poetry for Python apps.
3. Address the TODOs in the codebase. These are very descriptive! One concern is that our API doesn't yet have a detection mechanism for duplicate receipts. :)
4. Set up CICD through GH Actions.  Our CICD pipeline should always run our unit tests!
5. Set up reusable middleware for handling errors in our API (among other things).



