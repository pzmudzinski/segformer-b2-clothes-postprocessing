# Set base image (host OS)
FROM public.ecr.aws/lambda/python:3.11

ARG API_URL
ARG API_TOKEN

ENV API_URL=$API_URL
ENV API_TOKEN=$API_TOKEN

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install any dependencies
RUN pip install -r requirements.txt

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Specify the command to run on container start
CMD [ "app.handler" ]