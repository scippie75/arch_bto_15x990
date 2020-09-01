# Installation guide for installing Arch Linux on my BTO X-BOOK 15X990
These are my installation instructions on installing Arch Linux with i3 on my BTO X-BOOK 15X990. They are incomplete and you should look at my other repository called arch_bto_17cl63 for more information. That repo is also a bit outdated so make sure you use the Arch Wiki Installation Guide together with it.

Disclaimer: this document is Work In Progress. Do not use! I am not responsible for any damage or loss of business or profits or whatever. If you care about not breaking things: DO NOT USE! As I have noticed, things change a lot in time, so make sure you use the Arch Wiki as your guide!

## Getting started

Always use the Arch installation guide at [Arch Installation Guide](https://wiki.archlinux.org/index.php/Installation_guide). It changes regularly and some changes are really important.
Download the ISO from the [https://www.archlinux.org/download](Download) page and write it to a USB. Using dd is just fine for this task.
Boot the laptop with the USB. Booting in UEFI is just fine.

## Installing the base

The newer ISO supports 4K so you can read the text mode. If this is not the case for you, go to the [https://github.com/scippie75/arch_bto_15x990/blob/master/README-old.md](old instructions) for how to make your font bigger.

You should just follow the guide, but here is what I did (if any of the steps below show an unexpected result, don't go further):

    # rfkill
    ...
    2 wlan phy0 unblocked unblocked
    # iwctl
    [iwd]# device list
    wlan0 ...
    [iwd]# station wlan0 scan
    [iwd]# station wlan0 get-networks
    ...
    [iwd]# station wlan0 connect \<SSID\>
    # ping archlinux.org
    # timedatectl set-ntp true

Partitioning, I keep up to you. This is a very personal thing. Make sure you have an EFI partition (of at least 100MB) and a Linux Filesystem partition. I don't make a swap partition because I feel I don't need it with 32GB of memory.

    # mkfs.ext4 /dev/<linux filesystem partition>
    # mount /dev/<linux filesystem partition> /mnt
    # mkdir /mnt/efi
    # mount /dev/<EFI partition> /mnt/efi

You used to have to edit the mirrors list, but this is now generated and sorted automatically. Still though, it might be worth checking it out because this will be copied onto the new system.
Now we will install the base and the linux kernel. It is up to you to choose the default kernel or go for a [https://wiki.archlinux.org/index.php/Kernel](different kernel). If you want stability, go for LTS. Because this is my leasure laptop, I go for the cutting edge latest kernel. I added some extras because I have a Windows partition as well. I also need WIFI so I add that too (warning, I want my network to be available in the console, even before one of the desktop managers kicks in, if that's not what you want, do some research)

    # pacstrap /mnt base linux linux-firmware exfat-utils ntfs-3g dhcpcd connman wpa_supplicant bluez openvpn vim man-db man-pages texinfo
    # genfstab -U /mnt >> /mnt/etc/fstab
    # arch-chroot /mnt
    # ln -sf /usr/share/zoneinfo/Europe/Brussels /etc/localtime
    # hwclock --systohc
    
Edit /etc/locale.gen and uncomment en_US.UTF-8 UTF-8 and anything else you may need.

    # locale-gen
    # echo 'LANG=en_US.UTF-8' >/etc/locale.conf
    # echo 'myhostname' >/etc/hostname
    # echo '127.0.0.1	localhost' >/etc/hosts
    # echo '::1		localhost' >>/etc/hosts
    # echo '127.0.1.1	myhostname.localdomain	myhostname' >>/etc/hosts
    # passwd
    ...
    
## Boot loader

Before you reboot, you must make sure you can reboot.
    
    # pacman -Syu grub efibootmgr
    # grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB

The BTO laptops use a Clevo keyboard and if you want the backlight buttons to work, you need some kernel parameters. Edit /etc/default/grub and add 'acpi_osi=!' 'acpi_osi=Linux' (without the quotes) to the GRUB_CMDLINE_LINUX_DEFAULT line. You can also add 'nouveau.modeset=0' if you are planning to use nvidia prime with nvidia nonfree driver later and want to make sure there are no conflicts with the nouveau driver.
    
    # grub-mkconfig -o /boot/grub/grub.cfg
