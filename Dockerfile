# Use an official Python runtime as a parent image
FROM python:3.11
# Set the working directory in the container
WORKDIR /CADAssignment

# Copy the current directory contents into the container at /app
COPY . /CADAssignment/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "/CADAssignment/app.py"]
