# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY src/ /app

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python", "patient_record_service.py"]
