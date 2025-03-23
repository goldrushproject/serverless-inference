FROM python:3.12-slim

# Install the specified packages
RUN pip install --no-cache-dir -r shared/requirements.txt

# Copy function code and the additional logic file from the shared directory
COPY container_app/app.py .
COPY shared/logic.py ./shared/

# Expose the port your application will run on (if applicable)
EXPOSE 8080

# Trigger workflow

# Set the entry point for the container
CMD ["python", "app.py"]