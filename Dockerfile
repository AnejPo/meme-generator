# Base image – Python
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (Flask app)
EXPOSE 10000

# Set environment variable (optional)
ENV PORT=10000

# Command to run the app
CMD ["python", "app.py"]
