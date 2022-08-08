# Social Media App

## Guide

This repo has been created while following this [tutorial](https://www.youtube.com/watch?v=ToXOb-lpipM) by [Sanjeev Thiyagarajan](https://www.youtube.com/c/SanjeevThiyagarajan), modified to use MongoDB as the database.

## Objective

The objective of the repo is to create a twitter-like social media application backend using FastAPI and MongoDB.

## Tech Stack

The backend has been built on the following web technologies:

- API Framework: [FastAPI](https://fastapi.tiangolo.com)
- Database: [MongoDB](https://www.mongodb.com)
- Database Driver: [Motor](https://www.mongodb.com/docs/drivers/motor/)
- ODM: [Beanie](https://roman-right.github.io/beanie/)
- Web Server: [Uvicorn](https://www.uvicorn.org) and [Gunicorn](https://gunicorn.org)

## Deployment

### Creating Environment Variables

The simpler way is to create a `.env` file in the home directory and utilize that. However, we usually want to avoid this approach since the file can accidentally be uploaded to the repo. Alternatively:

- Place the `.env` file in the home folder `/home/ubuntu/`
- Edit the `.profile` file in the home folder with the following command so that it triggers automatically when the system is started:

```bash
set -o allexport; source /home/ubuntu/.env; set +o allexport
```

### Testing with Uvicorn

- Run:

```bash
uvicorn --host 0.0.0.0 app.main:app
```

- Test by going to `{Public IP}:8000` and `{Public IP}:8000/docs`

### Testing with Gunicorn

- Run:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

- Test by going to `{Public IP}:8000` and `{Public IP}:8000/docs`

- The output to the command should show 4 workers with 1 parent process

### Converting the API into a Service

- Get python path by executing `which gunicorn`

- Go to `/etc/systemd/system`

- Create a new file called `api.service` with the following:

```
[Unit]
Description=FastAPI server service
After=network.target

[Service]
User=ubuntu
Group=ubuntu # same as User
WorkingDirectory=/home/ubuntu/src # whatever is the location of your application folder
Environment="PATH=/home/ubuntu/bin" # the bin location you got from which gunicorn
EnvironmentFile=/home/ubuntu/.env # the location to the .env file
ExecStart=/home/ubuntu/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 # use the location you got from which gunicorn

[Install]
WantedBy=multi-user.target
```

- Note: the `.profile` edit to automatically import environment variables is no longer required

- Run: `sudo systemctl start api`

- Verify it is running with `sudo systemctl status api`

- Test by going to `{Public IP}:8000` and `{Public IP}:8000/docs`

- Run: `sudo systemctl enable api` to force the service to restart on reboot

### Setting up nginx

- Install nginx: `sudo apt install nginx -y`

- Start nginx: `sudo systemctl start nginx`

- Test by going to `{Public IP}` and it should show you an nginx welcome page

- Go to `/etc/nginx/sites-available` and open `default`

- Change the location block:

```
location / {
    proxy_pass http://localhost:8000;
    proxy_http_version 1.1;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $http_host;
    proxy_set_header X-NginX-Proxy true;
    proxy_redirect off;
}
```

- Run `sudo systemctl restart nginx`

- Test by going to `{Public IP}` and `{Public IP}/docs` and it should show you the API interface

### Attaching a domain name

- This requires you to have a domain name attached to the `{Public IP}`

- As an example, attach both `api.com` and `www.api.com` to the `{Public IP}` through DNS records

- Test by going to `api.com` and `api.com/docs`

- Test by going to `www.api.com` and `www.api.com/docs`

### Setting up an SSL certificate

- Go to Certbot instructions [page](https://certbot.eff.org/instructions)

- Select `nginx` and `Ubuntu 20`

- Follow the guide to setup the certificate

- Make sure port 443 is open for HTTPS requests

- Test by going to `api.com` and `api.com/docs`; the connection should be encrypted

- Repeat the test for `www.api.com`
