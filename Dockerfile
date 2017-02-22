FROM python:2.7

# Install Python modules from requirements.txt
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Install Samsara-Python from Git
RUN cd /src; pip install git+https://github.com/samsarahq/samsara-python.git

# Bundle app source
ADD . /src

# Expose port
EXPOSE 5000

# Run
CMD ["python", "/src/application.py"]