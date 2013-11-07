# -*- mode: ruby -*-
# vi: set ft=ruby :

# This Vagrantfile targets the vagrant-lxc provider. It should work on other providers given
# a relatively recent version of Vagrant, but your mileage may vary.

Vagrant.configure("2") do |config|
  config.vm.box = "wheezy64"

  config.vm.network :forwarded_port, guest: 8080, host: 8080, host_ip: '0.0.0.0'
  config.vm.network :forwarded_port, guest: 6379, host: 6379, host_ip: '0.0.0.0'
  config.vm.network :forwarded_port, guest: 8983, host: 8983
  config.vm.provision :shell, :inline => <<END
# Check if we need to perform a weekly upgrade - this also triggers initial provisioning
touch -d '-1 week' /tmp/.limit
if [ /tmp/.limit -nt /var/cache/apt/pkgcache.bin ]; then
    apt-get -y update
    apt-get -y dist-upgrade
    apt-get -y install redis-server sqlite3 htop tmux vim rsync python-dev python-setuptools python-pip python-pygments python-redis python-nose
fi
rm /tmp/.limit
END
end
