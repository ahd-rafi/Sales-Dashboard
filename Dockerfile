# Use Python 3.10 as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat (nc)
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the project files
COPY . .

# Copy the entrypoint.sh script to /app directory
COPY entrypoint.sh /app/entrypoint.sh

# Debugging step: List the /app directory to confirm the file was copied
RUN ls -l /app

# Make sure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Expose port 8000 for the Django app
EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#rafi new
