# INQUISITOR

---

## Virtual Machine Setup

This project requires three virtual machines:

- **Target VM:** Runs the FTP server.
- **Source VM:** Acts as the FTP client.
- **Inquisitor VM:** Used as the attacker.

**Recommended OS:** [Debian 12.11.0](https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.11.0-amd64-netinst.iso)  
**Virtualization:** Oracle VM VirtualBox

> **Tip:** Install VirtualBox Guest Additions for clipboard sharing and drag-and-drop.

### Shared Clipboard Configuration

Enable clipboard sharing for each VM:

- In VirtualBox, go to **Devices > Shared Clipboard > Bidirectional**.

### Root Access

Switch to root to avoid modifying the sudoers file:

```bash
su -
```

---

## VM Network Configuration

Configure all VMs to use DHCP for the NAT network:

```bash
sudo bash -c 'cat <<EOF > /etc/network/interfaces
# Network interfaces configuration

source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

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

2. For each VM, go to **Machine > Settings > Network**, set "Attached to" as **NAT Network**, and select your created network.  
    ![Screenshot of VM](https://github.com/ftTower/ftTower/blob/main/assets/Malcolm/vm_network.png)

Check connectivity between VMs:

```bash
ip a  # Get the IP addresses
ping <ip-of-source>
ping <ip-of-target>
```

---

# Preparation for Attack Demo

## Setting Up the FTP Server (Target VM)

Install and configure the FTP server:

```bash
sudo apt update && sudo apt install git vsftpd vim -y
sudo systemctl start vsftpd
sudo systemctl enable vsftpd
sudo systemctl status vsftpd
sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.original
```

Edit `/etc/vsftpd.conf` to enhance security and enable passive mode. Ensure these lines are present:

```ini
anonymous_enable=NO
local_enable=YES
write_enable=YES
chroot_local_user=NO
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=50000
xferlog_enable=YES
log_ftp_protocol=YES
```

Edit the file with:

```bash
sudo vim /etc/vsftpd.conf
```

Create a dedicated FTP user and set up the directory:

```bash
sudo adduser ftpuser
sudo mkdir -p /home/ftpuser/ftp_files
sudo chown ftpuser:ftpuser /home/ftpuser/ftp_files
sudo chmod 755 /home/ftpuser/ftp_files
sudo systemctl restart vsftpd
```

> **Note:** Remember the password set for `ftpuser`—you'll need it for FTP access.

---

## Testing the FTP Client (Source VM)

On the source VM, install the FTP client and create a test file:

```bash
sudo apt install ftp -y
echo "This is a test file from the client." > ~/client_test.txt
```

Connect to the FTP server (replace `<Target_IP>` with your target VM's IP):

```bash
ftp <Target_IP>
```

Login credentials:

- **Username:** `ftpuser`
- **Password:** (password set earlier)

Test file upload:

```ftp
cd ftp_files
put client_test.txt
ls
```

---

This setup ensures you have a working FTP server and client for practicing FTP-related cybersecurity exercises.

---

## Setting Up the Attacker VM (Inquisitor)

Install required packages and clone the project:

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install net-tools iputils-ping iproute2 -y
git clone https://github.com/ftTower/Piscine-Cybersecurity.git Piscine-Cybersecurity
cd Piscine-Cybersecurity/Inquisitor
echo done
```

---

You are now ready to begin your cybersecurity exercises with a properly configured environment.
