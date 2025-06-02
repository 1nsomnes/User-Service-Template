# Use an official Python runtime as a parent image
FROM python:3.12-bullseye

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables
# Note: DATABASE_URL should be provided through Kubernetes ConfigMap or secrets
ENV DATABASE_URL=mongodb://your-mongodb-uri:27017/userDatabase
ENV SECRET_KEY_TOKENIZATION=your-secret-key-tokenization
ENV SECRET_KEY_VERIFICATION=your-secret-key-verification
ENV EMAIL_SERVICE_URL=http://your-email-service-url

# Set additional environment configurations
ENV FLASK_APP=user_service.py
ENV FLASK_ENV=development

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

