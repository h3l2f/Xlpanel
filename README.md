<div align="center">
<h2>Xlpanel - A client for pterodactyl.</h2>
<img src="https://img.shields.io/badge/Version-0.2-0040ff.svg"></img>
<img src="https://img.shields.io/badge/Codename-sinii_khleb-0000aa.svg"></img>
<img src="https://i.imgur.com/MWZZ9qJ.png"></ing>
</div>

# Update: ver 0.2 (sinii khleb)
![v0.2](https://i.imgur.com/bwRUsJu.png)
> Now you can personalize your client with any color you want.

# Key features
* Manage your pterodactyl server
* Afk for coins
* Admin page
* Easy to use
* Customize your client with your favourite color

# Require
- Python 3.10 or higher.
- Libraries in `requirements.txt` file.

# Installation
<details>

<summary>Nginx Configuration</summary>

## If you are using nginx for webserver, you need to do this step before the main installation:

- Create a nginx's conf file:
``` bash
sudo touch /etc/nginx/sites-available/<name_you_want>.conf
```

- Paste this code into that file:
```conf
server {
    listen 80;
    listen [::]:80;
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name <server_name>;

    ssl_certificate <path_to_ssl_file>;
    ssl_certificate_key <path_to_cert_file>;

    location / {
        proxy_pass http://localhost:<port>;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header    X-Real-IP $remote_addr;
    }
}
```

- Link that file to `sites-enabled` folder:
```bash
sudo ln -s /etc/nginx/sites-available/<name_you_want>.conf /etc/nginx/sites-enabled/<name_you_want>.conf
```

- Restart the nginx:
    + ubuntu: `sudo systemctl restart nginx`
    + alpine: `sudo service restart nginx`

> Done. Now you can go to the main installation!

</details>

- Clone this project:
```bash
git clone https://github.com/h3l2f/xlpanel
```
- Go to the project folder
```bash
cd xlpanel
```
- Install the requirement libraries:
```bash
pip install -r requirements.txt
```
- Copy `config.example.json` to `config.json`:
```bash
cp config.example.json config.json
```
- Config the `config.json` file.
- Run the server:
```bash
python main.py
```
> Done. Now your server is online!

- To change the icon, please upload your icon into `statics/img` folder and replace the `logo.png` with your new icon.

# Pterodactyl theme
<img src="https://i.imgur.com/PL3CRTX.png"></ing>

* Now you can have a pterodactyl theme with our style for **free**!
> [!WARNING]
> Remember: Your pterodactyl need to have [Blueprint](https://blueprint.zip/) before you can apply the theme.

### **Enjoy your new client!**
