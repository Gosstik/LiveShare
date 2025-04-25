# Deploy

## VM (TODO)

Preferable settings (`Yandex Cloud`):

- 8GB HDD
- vCPU ???
- RAM: 4GB
- Not interruptible (to have permanent IP address)


Insert login (e.g. `admin`) + ssh key and wait for VM creation. Connect:

```bash
ssh admin@11.22.33.44 # use PUBLIC IPv4 VM IP
```

Next we have to create separate user for application.

```bash
APP_USER="liveshare"

sudo adduser "$APP_USER"
sudo usermod -aG sudo "$APP_USER"
su - "$APP_USER"
```


### Make ssh keys for cloning repo

```bash
USER_EMAIL="your_email@example.com"

mkdir -p ~/.ssh/github
ssh-keygen -t ed25519 -C "$USER_EMAIL"
# file to save key: ~/.ssh/github/ssh_key
```

Add data to `~/.ssh/config`:

```text
# GitHub.com
Host github.com
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/github/ssh_key
```

Alternative way if private key already exists:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

```bash
git clone ... # cloning repo(s)
```

### Install nginx

```bash
sudo apt-get update
sudo apt-get install nginx
sudo ufw allow 'Nginx HTTP' # enable firewall

sudo systemctl status nginx
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl enable nginx # enable autoload with VM start

sudo nginx -s reload
# TODO: search for command to check state
```

`nginx` configuration.

```bash
# main nginx config (we don't have to modify it)
vim /etc/nginx/nginx.conf

# /etc/nginx/conf.d/*.conf
# /etc/nginx/sites/enabled/*
# /etc/nginx/sites/available/*

APP_NAME=liveshare

vim "/etc/nginx/sites/available/$APP_NAME.prod.conf"
# Insert lines from the `nginx` config below and close vim

ln -s /etc/nginx/sites/available/$APP_NAME.prod.conf /etc/nginx/sites/enabled/$APP_NAME.prod.conf

vim /etc/nginx/sites/available/default # add include
# TODO: more details
```

`nginx` config:

```nginx
server {
  # some staff
  # ...

  ### For static files

  location /static/ {
    root /var/www/html;
  }

  ### For django

  location /api {
    proxy_pass http://localhost:8000/;
  }

  location /admin {
    proxy_pass http://localhost:8000/;
  }
}
```

### Other deps

```bash
sudo apt-get install tmux
```

<!----------------------------------------------------------------------------->

## Backend

Before deploying add IP to `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` and probably `INTERNAL_IPS`:

```python
ALLOWED_HOSTS = ['*'] # add specific IP
CORS_ALLOWED_ORIGINS = [
  'http://localhost:3000',
  'http://${ENV_VM_IP}',
]
```

### Install deps

```bash
sudo apt-get install python3.10-venv
python3 -m venv .venv
source .venv/bin/activate
cd Backend
pip install -r requirements.txt

# TODO: database + copy .env files

pip install gunicorn

tmux
# Simple way
./manage.py runserver 0.0.0.0:8000
# With wsgi
cd "$APP_NAME/Backend"
gunicorn --workers=2 Backend.wsgi

sudo systemctl status gunicorn
sudo journalctl -u gunicorn # more logs
sudo systemctl daemon-reload # update config
```

<!----------------------------------------------------------------------------->

## Frontend

!!! Change IP address from `127.0.0.1` to public IP address of VM (configure through `.env`).

```bash
cd Frontend
sudo apt-get install npm
npm -v
npm install

# NOTE: we will not use serve, it is just example
npm run build # build production code
sudo cp -r build/ /var/www
sudo mv html old_html
sudo mv build html
sudo npm install -g serve # install server for hosting static files
serve -s build # run service
```

## TODO

k8s
