ARG python_ver=python3.8

FROM mcr.microsoft.com/azure-functions/python:3.0-${python_ver}-buildenv AS img_pip_builder

# Doesn't have to do additional os package installation since gcc has included in buildenv image
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl \
#     apt-utils \
#     apt-transport-https \
#     build-essential \
#     gcc

COPY requirements.txt /

ENV HOME=/home

RUN pip install --user -r /requirements.txt

# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8-appservice
FROM mcr.microsoft.com/azure-functions/python:3.0-${python_ver}

COPY --from=img_pip_builder /home/.local /home/.local 

# Make sure scripts in .local are usable:
ENV PATH=/home/.local/bin:$PATH
ENV PYTHONPATH=/home/.local/lib/${python_ver}/site-packages:$PYTHONPATH

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# Copy all python project files except the requirements.txt since we don't need to do pip install in this image
COPY . /home/site/wwwroot/
RUN rm -Rf /home/site/wwwroot/requirements.txt