
## RT-communication-scripts


### Dependences

#### Ubuntu Linux Kernel version 4.4.89

Downloading:

	wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.4.89/linux-headers-4.4.89-040489_4.4.89-040489.201709270634_all.deb http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.4.89/linux-headers-4.4.89-040489-generic_4.4.89-040489.201709270634_amd64.deb http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.4.89/linux-image-4.4.89-040489-generic_4.4.89-040489.201709270634_amd64.deb

Installing:

	sudo dpkg -i linux-*

#### Linux Backports 4.4.2-1

Downloading:

	wget https://www.kernel.org/pub/linux/kernel/projects/backports/stable/v4.4.2/backports-4.4.2-1.tar.gz

Uncompress and edit QoS values for your wireless driver.

#### Others dependences

	sudo apt-get install libc6-dev build-essential


