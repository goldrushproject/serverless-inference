FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt from the shared directory
COPY ../shared/requirements.txt .

# Install the specified packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code and the additional logic file from the shared directory
COPY app.py .
COPY ../shared/logic.py ./shared/

# Expose the port your application will run on (if applicable)
EXPOSE 8080

# Set the entry point for the container
CMD ["python", "app.py"]