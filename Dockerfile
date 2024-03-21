FROM 3.9-alpine

COPY . /app
WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
