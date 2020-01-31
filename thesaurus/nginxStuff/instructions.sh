# Install and start Nginx
sudo apt install nginx
sudo systemctl start nginx
# configure server blocks
sudo vim /etc/nginx/sites-available/default
sudo vim /etc/nginx/sites-available/sproj.colehollant.com
sudo vim /etc/nginx/sites-available/sproj.api.colehollant.com
# enable them
sudo ln /etc/nginx/sites-available/sproj.colehollant.com /etc/nginx/sites-enabled/sproj.colehollant.com
sudo ln /etc/nginx/sites-available/sproj.api.colehollant.com /etc/nginx/sites-enabled/sproj.api.colehollant.com
sudo ln /etc/nginx/sites-available/sproj.model.colehollant.com /etc/nginx/sites-enabled/sproj.model.colehollant.com

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