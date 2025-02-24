# Use a stable Python image
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Copy project files
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Set execute permissions for the script
RUN chmod +x /app/entrypoint.sh

# Use the script as the container's entry point
ENTRYPOINT ["bash", "/app/entrypoint.sh"]

