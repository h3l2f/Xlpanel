<div align="center">
<h2>Xlpanel - A client for pterodactyl.</h2>
<img src="https://img.shields.io/badge/Version-1.0-0040ff.svg"></img>
<img src="https://img.shields.io/badge/Codename-novaya_veshsh-0000aa.svg"></img>
</div>

# Update: v1.0 (novaya veshsh)
> Just renew everything!

# Change logs: v1.0
- New UI
- New Experience

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

- Download the latest version
- Extract the .zip file
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

- To change the icon, please upload your icon into `assets/img` folder and replace the `logo.png` with your new icon.

<details>

<summary>How to change the theme?</summary>

- Edit the `sass/_data.scss` file
- You can change:
    + primary color: `$pcolor`
    + background color: `$bgcolor`
    + text color: `$text-color`
- After that, run the `bprj.py` to compile all the sass file into css.

</details>

# Pterodactyl theme
<img src="https://i.imgur.com/PL3CRTX.png"></ing>

* Now you can have a pterodactyl theme with our style for **free**!
> [!WARNING]
> Remember: Your pterodactyl need to have [Blueprint](https://blueprint.zip/) before you can apply the theme.

### **Enjoy your new client!**
