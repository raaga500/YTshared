FROM apache/superset
# Switching to root to install the required packages
USER root

# install FreeTDS and dependencies
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install freetds-dev -y \
 && apt-get install freetds-bin -y \
 && apt-get install tdsodbc -y \
 && apt-get install --reinstall build-essential -y \
 && apt-get install rpm2cpio -y \
 && apt-get install cpio -y

 # populate "ocbcinst.ini"
RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

# Install Dremio ODBC driver
RUN pip install pyodbc
RUN wget https://download.dremio.com/odbc-driver/1.5.4.1002/dremio-odbc-1.5.4.1002-1.x86_64.rpm

RUN rpm2cpio dremio-odbc-1.5.4.1002-1.x86_64.rpm | cpio -idmv
RUN mv opt/dremio-odbc /opt/dremio-odbc


# Example: installing the MySQL driver to connect to the metadata database
# if you prefer Postgres, you may want to use `psycopg2-binary` instead
RUN pip install mysqlclient
# Example: installing a driver to connect to Redshift
# Find which driver you need based on the analytics database
# you want to connect to here:
# https://superset.apache.org/installation.html#database-dependencies
#RUN pip install pydobc
RUN pip install sqlalchemy-redshift
RUN pip install sqlalchemy-dremio
RUN pip install pymssql
# Switching back to using the `superset` user
USER superset