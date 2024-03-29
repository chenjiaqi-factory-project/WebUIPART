# Source Image
FROM python:3.7
# Author
MAINTAINER Leon "leontian1024@gmail.com"
# Set working director
WORKDIR /var/app/webServerDir
# Add source code from os into container
Add . /var/app/webServerDir
# Import packages
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install Flask
RUN pip install Flask-wtf
RUN pip install psycopg2-binary
RUN pip install flask_login
RUN pip install pandas
RUN pip install flask_bootstrap
RUN pip install python-dotenv
# Expose port
EXPOSE 5000
# Run command
ENTRYPOINT ["python","./webServer.py"]

