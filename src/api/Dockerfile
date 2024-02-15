# Use a specific, slim variant of the Python 3.10 image for smaller image size
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Expose the port the app runs on
EXPOSE 3100

# Copy only the requirements file, to cache the pip install step
COPY ./requirements.txt /code/

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY ./api /code/api

RUN pip install debugpy

# Command to run the application
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "3100", "--proxy-headers"]
