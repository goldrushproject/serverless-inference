FROM python:3.12-slim

# Copy requirements.txt from the shared directory
COPY shared/requirements.txt .

# Install the specified packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code and logic to container
COPY container_app/app.py .
COPY --exclude=__pycache__ shared/ ./shared/

# Expose the port your application will run on (if applicable)
EXPOSE 8080

# Set the entry point for the container
CMD ["python", "app.py"]