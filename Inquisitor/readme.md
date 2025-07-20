### Installing Dependencies (on Malcolm VM)

Update and install required packages:

```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install -y 
git clone https://github.com/ftTower/Piscine-Cybersecurity.git Piscine-Cybersecurity
cd Piscine-Cybersecurity/Inquisitor
echo done
```

---

## VM Network Configuration

Configure the three VMs to use DHCP for the NAT network:

```bash
sudo bash -c 'cat <<EOF > /etc/network/interfaces
# This file describes the network interfaces available on your system
# and how to activate them. For more information see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto enp0s3
iface enp0s3 inet dhcp
EOF'
echo "Network configuration replaced. Implementing DHCP for NAT network."
sudo systemctl restart networking
clear && ip a
```

### Creating a NAT Network

1. In VirtualBox, go to **File > Tools > Network Manager > NAT Networks** and create a new NAT network.  
    ![Screenshot of Vbox](https://github.com/ftTower/ftTower/blob/main/assets/Malcolm/Vbox_NAT_network.png)

2. For three VMs, go to **Machine > Settings > Network**, set "Attached to" as **NAT Network**, and select your created network.  
    ![Screenshot of VM](https://github.com/ftTower/ftTower/blob/main/assets/Malcolm/vm_network.png)
