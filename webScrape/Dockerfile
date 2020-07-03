# Python 3.6.7
FROM python:3

# author of file
LABEL maintainer="Andrew Pollack <andrewpkq@gmail.com>"

# Packages that we need 
WORKDIR /app

# Copy requirements
COPY requirement.txt /app

# instruction to be run during image build
RUN pip install -r requirement.txt

# Mount volume
VOLUME /app/data

# Docker container in /app directory 
COPY . /app

# In this case we want to start the python interpreter
ENTRYPOINT ["python"]

# Argument to python command
CMD ["scraping.py"]

# docker build -t reddit_wow_scrape:test .
# docker run -t reddit_wow_scrape:test
