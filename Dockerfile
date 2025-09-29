# Use official Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /src

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose port the app will run on
EXPOSE 3001

# Command to run the app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3001"]
