FROM python:3.10

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat (nc)
RUN apt-get update && apt-get install -y netcat-openbsd


# Copy project files
COPY . .

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Expose port
EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
