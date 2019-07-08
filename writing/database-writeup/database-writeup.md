# DB Writeup

## What's all this then

I'd like to keep all the thesaurus entries in a database, and be able to interface with that via some API. While we could do everything locally and save some of the configuration headache, we also would hardly be able to use it. So, in the pursuit of functionality, we'll need a server to put this on. I chose [DigitalOcean](https://www.digitalocean.com), a popular cloud services platform among other names like AWS and Azure. Surely we will also be using DigitalOcean for hosting the rest of this as well :)

## Don't be root!

It should go without saying that it's wise to stray from doing all things as `root`. As default, we can only `ssh` into `root`, so we must add a user! We'll still need root access, so we'll be sure to add our new user to the `sudo` group. Then to finish this setup, we must patch up our `ssh` configuration: we want to `ssh` into the new user and disable `ssh` into `root`.

```sh
ssh root@<IP_ADDRESS>
adduser <USERNAME>
usermod -aG sudo <USERNAME> 
rsync --archive --chown=<USERNAME>:<USERNAME> ~/.ssh /home/<USERNAME> 
vim /etc/ssh/sshd_config    (set "PermitRootLogin" to "no")
```

Of course, we'll make a nice `ssh` config on our personal machine for our convenience. We'd like to save the hassle of keeping track of IP addresses and users and keys, so we'll make another entry to be able to simply run `ssh sproj`.

## Quick Firewall stuff

Gonna need to allow access to our droplet
```sh
sudo ufw reload
sudo ufw allow 8080 (8000, 80, 3000)


```

## The big whale upstairs

There is certainly a warranted section on Docker.