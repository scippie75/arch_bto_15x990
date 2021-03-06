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

    # pacstrap /mnt base linux linux-firmware intel-ucode exfat-utils ntfs-3g dhcpcd connman wpa_supplicant bluez openvpn vim man-db man-pages texinfo
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
    
    # pacman -Syu grub efibootmgr os-prober
    # grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB

The BTO laptops use a Clevo keyboard and if you want the backlight buttons to work, you need some kernel parameters. Edit /etc/default/grub and add 'acpi_osi=!' 'acpi_osi=Linux' (without the quotes) to the GRUB_CMDLINE_LINUX_DEFAULT line. You can also add 'nouveau.modeset=0' if you are planning to use nvidia prime with nvidia nonfree driver later and want to make sure there are no conflicts with the nouveau driver.

Also, on the 4K screen, it might be useful to change the GRUB_GFXMODE value from auto to 1024x768.
    
    # grub-mkconfig -o /boot/grub/grub.cfg

See that your linux image is found. If you have a Windows partition and it is not found, you may have forgotten to install ntfs-3g and os-prober. Use pacman to install it now.

    # exit
    # reboot

Remove the USB stick when the system reboots.

## Safe or fast

One can argue whether you should now immediately create a user account and work with that one. I am all for it, except when installing the basic systems. At that point, it is just handy to be root. I will go on as being root, but you go ahead and create a user and use sudo.

## Setting up the WIFI

    # systemctl enable connman
    # systemctl start connman
    # connmanctl technologies
    
This last command should now show your ethernet, bluetooth and wifi device and whether it is powered on. To power on the wifi:

    # connmanctl enable wifi
    
Now you should be able to set up the wifi. If you use a protected network, you need the cli interface, otherwise it is possible to use commands directly on connmanctl.

    # connmanctl
    connmanctl> agent on
    connmanctl> scan wifi
    connmanctl> services
    connmanctl> connect wifi_... (use tab completion to help you identify the right network)
    connmanctl> quit
    # connmanctl state
    ... should show online
    # ip a
    ... should show that your wifi interface has an IP number
    # ping archlinux.org
    
Settings are stored in /var/lib/connman, so if you reboot, the network should still be configured correctly. You may want to try it.

## Installing the useful stuff

At this point of the guide, we will be looking at [General recommendations](https://wiki.archlinux.org/index.php/General_recommendations) which you should follow. You may want to do this for yourself and only look at the specific BTO things below.

### SSD periodic trimming

You only need this if you have SSD disks, but in that case, you really should do it to make sure your disk stays usable.
    
    # pacman -Syu util-linux
    # systemctl enable fstrim.timer
    # systemctl start fstrim.timer

### Pulse audio

Not at all necessary, but it is more fun in my opinion.

    # pacman -Syu pulseaudio alsa-utils pulseaudio-alsa bluez bluez-utils pulseaudio-bluetooth
    # systemctl enable bluetooth.service
    # systemctl start bluetooth.service

For bluetooth support in pulseaudio, add the following lines to /etc/pulse/system.pa:
    
    load-module module-bluetooth-policy
    load-module module-bluetooth-discover

A reboot may be necessary

### Conserving power

You can conserve more power by setting /etc/tmpfiles.d/energy_performance_preference.conf

    w /sys/devices/system/cpu/cpufreq/policy?/energy_performance_preference - - - - balance_power

Save power on intel sound card, by setting /etc/modprobe.d/audio_powersave.conf

    options snd_hda_intel power_save=1

Save power with pulseaudio, edit /etc/pulse/system.pa and add (this may already be there):

    load-module module-suspend-on-idle

Saving power on bluetooth must be done manually:

    # rfkill block bluetooth

And you can disable it at boot in /etc/udev/rules.d/50-bluetooth.rules

    # disable bluetooth
    SUBSYSTEM=="rfkill", ATTR{type}=="bluetooth", ATTR{state}="0"

You can study power usage even further by installing powertop

    # pacman -Syu powertop
    # powertop

You can there do all the recommendations by setting the BAD stuff to GOOD, but this can be automated by creating a service for it. Put this in the file /etc/systemd/system/powertop.service

    [Unit]
    Description=Powertop tunings
    
    [Service]
    Type=oneshot
    ExecStart=/usr/bin/powertop --auto-tune
    
    [Install]
    WantedBy=multi-user.target    

Enable and start this service. Now the optimal power settings will be set after boot.

If you have non-SSD disks in the laptop, further power-saving measures can be taken by slowing down writing cached data to disk, slowing down the spin-up rate of the motors, etc. See [https://wiki.archlinux.org/index.php/Power_management#Writeback_Time](Power Management, writeback time) and things around it.

## Graphical environment

### Set up graphics adapter(s)

#### nvidia only (not using the hybrid graphics)

This model has two graphics adapters, an Intel and an Nvidia. The Intel uses less power, the Nvidia has more performance. You can use both combined with Nvidia prime, but it currently has performance problems (lower performance on both adapters and problems with anti-aliasing on the Nvidia adapter).
So if you only care about performance, not about power, this may be your preferred choice. Beware that the nvidia fan will spin up a lot though.

If 32-bit (Steam) is needed, enable the [https://wiki.archlinux.org/index.php/Official_repositories#multilib](multilib repository).

First install intel:

    # pacman -Syu nvidia nvidia-prime nvidia-utils lib32-nvidia-utils
    # pacman -Syu i3-gaps terminator lightdm lightdm-gtk-greeter i3status

See https://wiki.archlinux.org/index.php/NVIDIA_Optimus for these instructions:

Install the nvidia driver as instructed in the Arch Wiki and also install xorg-xrandr
Save these settings to /etc/X11/xorg.conf.d/10-nvidia-drm-outputclass.conf
```
Section "OutputClass"
    Identifier "intel"
    MatchDriver "i915"
    Driver "modesetting"
EndSection

Section "OutputClass"
    Identifier "nvidia"
    MatchDriver "nvidia-drm"
    Driver "nvidia"
    Option "AllowEmptyInitialConfiguration"
    Option "PrimaryGPU" "yes"
    ModulePath "/usr/lib/nvidia/xorg"
    ModulePath "/usr/lib/xorg/modules"
EndSection
```

If you are not using a Display Manager, then add these lines to ~/.xinitrc
```
xrandr --setprovideroutputsource modesetting NVIDIA-0
xrandr --auto
```
Otherwise, look up how to do this inside your Display Manager. If it is LightDM, then create the script /etc/lightdm/display_setup.sh
```
#!/bin/sh
xrandr --setprovideroutputsource modesetting NVIDIA-0
xrandr --auto
```
Make sure it is executable: sudo chmod +x /etc/lightdm/display_setup.sh
And make sure it is called from /etc/lightdm/lightdm.conf
```
[Seat:*]
display-setup-script=/etc/lightdm/display_setup.sh
```

#### intel+nvidia hybrid graphics

If you want balanced power usage, low power and silent fan on normal usage, high power and noisy fan on heavier usage, but (currently) with always a penalty on both graphics adapters, you can use nvidia-prime.

If 32-bit (Steam) is needed, enable the [https://wiki.archlinux.org/index.php/Official_repositories#multilib](multilib repository).

First install intel:

    # pacman -Syu mesa lib32-mesa vulkan-intel
    # pacman -Syu nvidia nvidia-prime nvidia-utils lib32-nvidia-utils
    # pacman -Syu i3-gaps terminator lightdm lightdm-gtk-greeter i3status

Actually, I didn't install lightdm-gtk-greeter, but chose for lightdm-slick-greeter (which works great on HiDPI screens), but this is only available in the AUR. This also makes it easy to immediately install other stuff from the AUR.
    
    # yay -Syu i3-gaps terminator lightdm lightdm-slick-greeter i3-scrot i3status

You need to manually edit /etc/lightdm/lightdm.conf, adding this under the [Seat:*] section:

    greeter-session=lightdm-slick-greeter

To enable automatic HiDPI scaling in i3 and some other nice stuff I stole from Manjaro, copy the .Xresources file in this repository to your home folder. Change the Xft.dpi value on the first line to whatever dpi you like. For best results, it should be a multiple of 96 though.

A good startup for an i3 config file is also in this repo (WIP) and must be copied to $HOME/.config/i3/config

## Very specific setup

### Create SSH tunnel with another computer

You should make sure to use a ssh public/private key pair. Create one specifically for a 'tunnel' user on the other computer and make sure that tunnel user has the least rights possible. Copy the private key to /root with a descriptive name.

To make a stable tunnel, we will need autossh:

    # pacman -Syu openssh autossh
    
To make it a systemd service, let's create one, create the /etc/systemd/system/tunnel.service with the contents:

    [Unit]
    Description=AutoSSH Tunnel with h1p
    After=dhcpcd.service
    
    [Service]
    ExecStart=/usr/bin/autossh -M 0 -T -N -o 'ServerAliveInterval 30' -i /root/private-key-for-tunnel -L <port>:localhost:<port> ... tunnel@<server-ip>
    ExecStop=killall -s KILL autossh
    RestartSec=10sec
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target
    
We use dhcpcd.service as trigger to activate this service, but as it takes time for wifi to connect, this won't work in most situations and the service will fail. To make sure it is retried when the connection is up, we add the RestartSec=10sec and the Restart=on-failure pulseaudio alsa-utils pulseaudio-alsaparameters. These will make sure that the connection is retried after 10 seconds. This may even remove the autossh requirement, but I like autossh too much to remove it.

Reboot and check after around 10 seconds: watch systemctl status tunnel.service

### Yay

As I like to use packages from the AUR, it's handy to have the comfort to install them easily in the same way as pacman works.
That's why I installed [https://aur.archlinux.org/packages/?O=0&K=yay](yay).
    # pacman -Syu git
    # git clone https://aur.archlinux.org/yay.git
    # cd yay
    # makepkg -cris
    # cd ..
    # rm -rf yay

From now on, you can just type yay instead of pacman. Yay will do everything pacman does (I don't know that for sure, but in the last 3 years that seemed to be the case for me) and will easily build and install AUR packages for you as well.

### Set keyboard repeat rate (for X11, not for TTY)

I find the best location to do this is to do this as early as possible and as user-independant as possible. Some people might prefer to have different values for different users. In that case, do the command in a local startup file, this may even be the i3 config, but ~/.xinitrc is fine too.

Otherwise, create a file in /etc/X11/xinit/xinitrc.d/99-keyboard.sh and make sure it is executable (chmod +x)

    #!/bin/sh
    /usr/bin/xset r rate 300 50

### Automatically detect external monitor connection and execute script to set it up correctly

Create a file /etc/udev/rules.d/60-drm.rules with contents:

    SUBSYSTEM=="drm", ACTION=="change", RUN+="/usr/local/bin/ext-monitor.sh"

Create the script-file /usr/local/bin/ext-monitor.sh with contents:

    #!/bin/sh
    HDMI_STATUS=`cat /sys/class/drm/card1-HDMI-A-1/status`
    if [ $HDMI_STATUS = "connected" ]
    then
	    DISPLAY=:0 /usr/bin/xrandr --output eDP-1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-1-0 --off --output DP-1-1 --off --output DP-1-2 --off --output DP-1-3 --off --output HDMI-1-0 --mode 1920x1080 --pos 0x0 --rotate normal --output DP-1-4 --off --output DP-1-5 --off --output DP-1-6 --off
    else
        DISPLAY=:0 /usr/bin/xrandr --output eDP-1 --primary --mode 3840x2160 --pos 0x0 --rotate normal --output DP-1-0 --off --output DP-1-1 --off --output DP-1-2 --off --output DP-1-3 --off --output HDMI-1-0 --off --output DP-1-4 --off --output DP-1-5 --off --output DP-1-6 --off
    fi

The xrandr parameters were generated by arandr when the setup was like I wanted it. You could call the arandr generated scripts directly so that if you change them, this will work instantly.
Don't forget the DISPLAY=:0 however to make sure the correct display is changed.
