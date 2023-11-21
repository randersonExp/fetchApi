# Use the official Python base image
FROM python:3.8

RUN mkdir /app

# Create our directory so we can copy everything over
RUN mkdir /app/fetchApi

# Copy all files from the current directory
COPY . /app/fetchApi/

WORKDIR /app/fetchApi/api

# Install the Python dependencies
RUN pip install -r requirements.txt

# Expose the port on which the application will run
EXPOSE 80

WORKDIR /app

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "fetchApi.api.main:createApp", "--host", "0.0.0.0", "--port", "80"]
