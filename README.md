# Installation guide for installing Arch Linux on my BTO X-BOOK 15X990
These are my installation instructions on installing Arch Linux with i3 on my BTO X-BOOK 15X990. They are incomplete and you should look at my other repository called arch_bto_17cl63 for more information. That repo is also a bit outdated so make sure you use the Arch Wiki Installation Guide together with it.

Disclaimer: this document is Work In Progress. Do not use! I am not responsible for any damage or loss of business or profits or whatever. If you care about not breaking things: DO NOT USE! As I have noticed, things change a lot in time, so make sure you use the Arch Wiki as your guide!

## Making the Clevo keyboard backlight work so you can at least use the Fn-button combinations and you are able to dim the backlight or even turn if off

  sudo vim /etc/default/grub
  -> Search for the line with GRUB_CMDLINE_LINUX_DEFAULT and append ' acpi_osi=! acpi_osi=Linux' (without quotes) in its value
  sudo grub-mkconfig -o /boot/grub/grub.cfg

Reboot and the controls should work.

## Change the brightness of the OLED screen
This is impossible as an OLED screen no longer has a backlight. Every pixel is its own LED light, which looks great.
There is a solution though: you can ask X to change the brightness of every pixel with xrandr.
Lowering the brightness works as good and also saves power, just light it did with a backlight.

Use the backlight.py script in this repository, bind it to your Fn-backlight keys (for example with +0.05 and -0.05 for up and down). Use its output value (is also shown without parameters) to show the current brightness on a status bar like i3blocks.
