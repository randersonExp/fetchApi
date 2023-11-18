# Project Overview 
Insert description here

# Running the Project via Docker Container
1. cd into the `/api` folder `cd api/`
2. Build the image locally and give it the tag `fetchapi` like so:
```
docker build -t fetchapi .
```

3. Run the container and turn on port forwarding. For testing, I used port 8000 like so:
```
docker run -d -p 8000:80 fetchapi
```

4. At this point, you should have a running container and you should be able to get a successful liveliness check by 
navigating to the following in your web browser: `http://127.0.0.1:8000/`.
