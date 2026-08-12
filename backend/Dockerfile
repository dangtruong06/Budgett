
FROM python:3.12-slim

# APP DIRECTORY
WORKDIR /app

# COPY DEPENDENCIES
COPY requirements.txt .

# INSTALL DEPENDENCIES
RUN pip install --no-cache-dir -r requirements.txt

# COPY CODE
COPY . . 

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]