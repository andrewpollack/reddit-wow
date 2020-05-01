# Python 3.6.7
FROM python:3

# author of file
LABEL maintainer="Andrew Pollack <andrewpkq@gmail.com>"

# Packages that we need 
WORKDIR /app

# Docker container in /app directory 
COPY . /app

# instruction to be run during image build
RUN pip install -r requirement.txt

# Mount volume
VOLUME /app/data

# In this case we want to start the python interpreter
ENTRYPOINT ["python"]

# Argument to python command
CMD ["pyDev/scraping.py"]
