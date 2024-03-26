# Use a specific, slim variant of the Python 3.11 image for smaller image size
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Expose the port the app runs on
EXPOSE 3100

# Copy only the requirements file first, to cache the pip install step
COPY ./api/requirements.txt /code/api/
RUN pip install -r /code/api/requirements.txt

# Now copy the rest of the application, this step will not invalidate the pip install cache 
# unless the requirements.txt file changes
COPY ./api /code/api
COPY ./common /code/common

# Install debugpy if necessary for debugging; consider whether this is needed for production
RUN pip install debugpy

# Command to run the application
CMD ["uvicorn", "api.api.app:app", "--host", "0.0.0.0", "--port", "3100", "--proxy-headers"]
