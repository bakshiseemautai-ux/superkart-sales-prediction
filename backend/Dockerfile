FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the container's working directory
COPY . .

# Install dependencies without cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Serve the Flask app (app.py -> superkart_api) with 4 Gunicorn workers on port 7860
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
