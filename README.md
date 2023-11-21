# Project Overview 
This project is a FastAPI implementation of the challenge posted [here](https://github.com/fetch-rewards/receipt-processor-challenge). FastAPI is something I've enjoyed using recently since it supplies the simple syntax of Python, while having performance and scalability in the same ballpark as Node and Go for I/O bound APIs. Since Python is the premier language for ML/DS solutions, this also makes it an ideal candidate when developing APIs and tooling alongside machine learning engineers! 

# Running the Project via Docker Container
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
