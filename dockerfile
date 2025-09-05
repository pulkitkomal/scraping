# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    p7zip-full \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install necessary Playwright dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libxss1 \
    libxcomposite1 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libgtk-3-0 \
    libasound2 \
    libgbm-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Install Playwright browsers
RUN playwright install

# Specify the command to run your tests
CMD ["python", "main.py"]