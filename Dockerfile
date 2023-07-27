# FROM python:3.7.12-slim-bullseye

# WORKDIR /usr/src/app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# 
# FROM python:3.9
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# Required for msodbcsql17 and mssql-tools
# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
# RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
# RUN apt-get update

# RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    # ACCEPT_EULA=Y apt-get install -y mssql-tools && \
    # echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
    # source ~/.bashrc && \
    apt-get install -y unixodbc-dev
    # apt-get install -y libgssapi-krb5-2  ## this is for slim distribution

## for pyodbc
RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get -y install g++ \
  && apt-get -y install unixodbc unixodbc-dev \
  && apt-get clean

## for gridfs lib to install fuse if came error apt-get install python-llfuse-doc
RUN apt-get install -y libfuse-dev 
    # && \
    # apt-get install python-llfuse-doc

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code/

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]