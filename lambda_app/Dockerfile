FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt from the shared directory
COPY ../shared/requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code and the additional logic file from the shared directory
COPY app.py ${LAMBDA_TASK_ROOT}
COPY ../shared/logic.py ${LAMBDA_TASK_ROOT}/shared/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ]