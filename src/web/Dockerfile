# Use a specific, slim variant of the Python 3.11 image for smaller image size
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Expose the port the app runs on
EXPOSE 3000

# Copy only the requirements file, to cache the pip install step
COPY ./requirements.txt /code/

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY ./web /code/web

# Set environment variables
# Flask runs in production mode by default. Use development if you need debug features.
ENV FLASK_APP=web/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=3000

# Command to run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=3000"]
