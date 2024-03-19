# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# First copy only the requirements file and install dependencies
COPY ./load/requirements.txt /code/load/
RUN pip install -r /code/load/requirements.txt

# Then copy the rest of the code
COPY ./load /code/load
COPY ./common /code/common
COPY ./files /code/files

# Run load.py when the container launches
CMD ["python", "-m", "load.load.load"]
