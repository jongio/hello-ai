# Use a specific, slim variant of the Python 3.10 image for smaller image size
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Expose the port the app runs on
EXPOSE 3000

# Copy only the requirements file, to cache the pip install step
COPY ./requirements.txt /code/

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY ./quote /code/quote

# Set environment variables
# Flask runs in production mode by default. Use development if you need debug features.
ENV FLASK_APP=quote/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=3000

# Command to run the application
CMD ["flask", "run"]
