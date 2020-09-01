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
    # 
