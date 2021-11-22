# Instructions

Step-by-step instructions on how to install Arch Linux properly on a VirtualBox VM

## Basic Info
- We will use UEFI, GRUB, and GPT to boot
- We will use only one drive (/dev/sda) and partition it into three parts, EFI System, Linux x86_64 root, and SWAP
- we will install a window manager, compositor, terminal, display manager, and program runner for our GUI environment

---

## Table of Contents
- [Create the VM](#create)
- [Boot into Shell](#boot)
- [Checks](#check)
- [Update System Clock](#clock)
- [Partition](#partition)
- [Mount](#mount)
- [Packages](#packages)
- [Chroot](#chroot)
- [Locale and Hostname](#locale)
- [Users](#users)
- [Bootloader](#bootloader)
-

---

## Create the VM <a name = "create"></a>

Open VirtualBox and create a new VM. Call it anything you want, I will call it **Awesome Arch**. If you do not have a free virtual disk image create one with at least 10GB. Once you have created your VM, go to Settings and do the following: increase the video memory to 128MB, turn on EFI Mode, and add the archlinux ISO to the empty disc drive. Save and start your VM.

## Boot into Shell <a name = "boot"></a>

Once your VM starts, go into *Arch Linux install medium (x86_64 UEFI)* mode, usually the first mode. If you do not press Enter, it will automatically use this boot mode after 15 seconds. 

## Checks <a name = "check"></a>

Check that your shell works!
You should be connected to the internet. If you enter:
`ping archlinux.org`
you should receive packets successfully
Verify your boot mode with:
`ls /sys/firmware/efi/efivars`
If this commands does not print an error, you are in EFI mode!

## Update System Clock <a name = "clock"></a>

Just enter:
`timedatectl set-ntp true`
and verify the minutes with:
`timedatectl status`
It will not align with your timezone but the minutes should match up

## Partition <a name = "partition"></a>

<span style="color:red"> Please follow these instructions carefully and exactly unless you do ***know what you are doing*** </span>

Check the name of the disk you want to partition with `fdisk -l`
In our case it should be `/dev/sda`

We can create a partition table using `fdisk /dev/sda` which will launch us into a fdisk prompt
We will create three partitions, one for the EFI system, one for SWAP, and one for our root
Follow these commands in order:
- `g` to create a GPT scheme table
- `n` to create the first partition, which will be the EFI System
- Press Enter until it gets to the last sector, in which we will enter `+1G`, then Enter
- `t` to change the partition's type, then Enter  
- `1` to make the first partition and EFI System
- `n` to create the SWAP partition
- Press Enter until the last sector, enter `+1.5G`, then Enter
- `t` to change this partition to swap, then Enter
- `19` to make partition Linux Swap
- `n` for last partition, press Enter all the way through
- `t` to make partition Linux Root (x86_64), Enter, `23`
- `p` to check our partition table
- If it looks correct, enter `w`
- If not, simply enter `q` and restart

Check your table with `fdisk -l /dev/sda`

## Mount <a name = "mount"></a>

Before we mount we need to make our partitions the right type

Currently, our partitions should be:
- /dev/sda1: EFI Boot
- /dev/sda2: Linux Swap
- /dev/sda3: Linux root (x86_64)

Run these commands:
```
mkfs.ext4 /dev/sda3
mkfs.fat -F32 /dev/sda1
mkswap /dev/sda2
```
Mount your partitions using the `mount` command

We can mount these as follows:
```
mount /dev/sda3 /mnt
mkdir /mnt/boot
mount /dev/sda1 /mnt/boot
swapon /dev/sda2
```
## Packages <a name = "packages"></a>

We need to install all the software and firmware we need to actually run Arch Linux. Along the way we will need several tools that we can install here. Optionally you can install these after you chroot into the system, but I do it here so I don't forget

***INSTALL ALL OF THESE PACKAGES***
```
pacstrap /mnt base linux linux-firmware sudo zsh python3 rust lua perl ruby nodejs npm vim neovim neofetch tldr man-db man-pages htop nmap dhcpcd inetutils netctl gnupg gzip grub efibootmgr intel-ucode
```
Wait. It takes time.

## Chroot <a name = "chroot"></a>

This part isn't too hard. Just don't forget anything

Just run these commands in order!
```
genfstab -U /mnt >> /mnt/etc/fstab # Only run this once
arch-chroot /mnt
```
## Locale and Hostname <a name = "locale"></a>

Run a few more commands. Change some of these for your location and language settings
```
ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime # Find your timezone
hwclock --systohc # Set the clock based on the timezone
vim /etc/locale.gen ~> (in vim) 177gg x :wq # Will allow en_US.UTF-8 encoding
locale-gen # Generates the specified locales from the previous command
echo 'LANG=en_US.UTF-8' > /etc/locale.conf # Enters the generated locale into the config
echo 'solarflare' > /etc/hostname # Choose any hostname you want
vim /etc/hosts ~> (add these three lines in vim to connect hosts to IP addresses)
	127.0.0.1    localhost
	::1          localhost
	127.0.1.1    solarflare.localdomain solarflare
~> :wq
```
## Users <a name="users"></a>

Create users and passwords, add them to groups, and give them sudo access
```
passwd ~> (Enter a root password when it asks, and then again)
useradd -G wheel,video,audio -m jeshwin # Or your name
passwd jeshwin # set user password
EDITOR=vim visudo ~> add 'jeshwin ALL=(ALL) ALL' under 'root ALL=(ALL) ALL' and uncomment '%wheel ALL=(ALL) ALL' ~> :wq
```
## Bootloader <a name = "bootloader"></a>

Install the GRUB bootloader and secure the config
```
grub-install --target=x86_64-efi --efi-directory=/boot/ --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg
```
## Configure Internet <a name = "internet"></a>

*REBOOT YOUR SYSTEM* and log back in as root
you should have all your packages but not be connected to internet
run these commands to configure the dhcpcd server and services
```
cp /etc/netctl/examples/ethernet-dhcp /etc/netctl
vim /etc/netctl/ethernet-dhcp ~> uncomment first line containing 'dhcpcd' and replace etho with enp0s3
systemctl enable dhcpcd
systemctl enable systemd-resolved
systemctl enable systemd-networkd
# ^^^ enables the dhcpcd and network services
systemctl start dhcpcd systemd-resolved systemd-networkd
# ^ starts the services so that we can connect to the internet
ping archlinux.org # Check if you can succcessfully ping the IP
```

## Window Manager <a name = "wm"></a>

Reboot and sign in through your user, **not root**
Install the window manager software needed and move config files:
`sudo pacman -S lightdm awesome xterm rofi picom nitrogen base-devel ttf-roboto`
Now just make sure our configs are correct:
`vim /etc/lightdm/lightdm.conf ~> under [SEAT:*] uncomment autologin-user and autologin-session and add your username and 'awesome' respectively ~> :wq`
Add jeshwin into the autologin group
`sudo groupadd -r autologin && sudo gpasswd -a jeshwin autologin`
Enable the lightdm service
`sudo systemctl enable lightdm.service`
Move the default awesome config to the .config directory at home:
`mkdir .config/awesome/ && cp /etc/xdg/awesome/examples/rc.lue ~/.config/awesome/`

## Test and Check <a name = "end"></a>

Test if your computer works by shutting down your VM, removing your ISO disk from the DVD slot in VM settings, and starting your machine again. After selecting the first option in the bootloader options, a desktop should start. That means your install was successful!
