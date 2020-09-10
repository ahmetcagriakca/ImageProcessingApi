# mssql-python3.6-pyodbc
# Python runtime with pyodbc to connect to SQL Server# Python runtime with pyodbc to connect to SQL Server
FROM ahmetcagriakca/tensorflow:base
ARG         PIP_URL_PRIVATE
RUN         echo "Python repository url: $PIP_URL_PRIVATE"
RUN         pip3 install  --upgrade pip
COPY       	./requirements.txt /app/requirements.txt
WORKDIR    	/app

RUN 		pip3 install   -r requirements.txt 
RUN         pip3 list
COPY       	. /app
WORKDIR    	/app
RUN python3 --version

ENTRYPOINT 	["python3"]
CMD 		["startup.py"]