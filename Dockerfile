FROM python:2.7

# Install Python modules
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Bundle app source
ADD . /src

# Expose port
EXPOSE 5000

# Run
CMD ["python", "/src/application.py"]