# Install and start Nginx
sudo apt install nginx
sudo systemctl start nginx
# configure server blocks
sudo vim /etc/nginx/sites-available/default
sudo vim /etc/nginx/sites-available/project.mydomain.com
sudo vim /etc/nginx/sites-available/project.api.mydomain.com
# enable them
sudo ln /etc/nginx/sites-available/project.mydomain.com /etc/nginx/sites-enabled/project.mydomain.com
sudo ln /etc/nginx/sites-available/project.api.mydomain.com /etc/nginx/sites-enabled/project.api.mydomain.com
sudo ln /etc/nginx/sites-available/project.model.mydomain.com /etc/nginx/sites-enabled/project.model.mydomain.com

# check syntax and reload
sudo nginx -t 
sudo systemctl reload nginx

# MAKE SURE THAT YOU'VE SET UP A RECORDS ON DIGITALOCEAN AND GOOGLE LOLL

# SSL [here](https://medium.com/@jgefroh/a-guide-to-using-nginx-for-static-websites-d96a9d034940)

sudo apt-get install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx
sudo certbot --nginx certonly