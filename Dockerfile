FROM python:3.11.9-alpine AS builder

WORKDIR /todo_flask

RUN apk update && apk add --no-cache \
    build-base \
    libpq \
    postgresql-dev

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache/pip



FROM python:3.11.9-alpine AS runner_dev

WORKDIR /todo_flask

RUN apk update && apk add --no-cache \
    libpq

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .
RUN ls
RUN chmod +x entrypoint_dev.sh
EXPOSE 5000
ENTRYPOINT [ "flask" ] 
CMD [ "--app", "app" , "run", "--host=0.0.0.0", "--debug" ]