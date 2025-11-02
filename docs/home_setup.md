# Some useful Info For Home Setup

## Power Management
[NUT Setup Instructions](https://www.jeffgeerling.com/blog/2025/nut-on-my-pi-so-my-servers-dont-die)  
<br>

setup deps on server:
```bash
sudo apt install -y libusb-1.0-0-dev libsnmp-dev libneon27-dev libavahi-client-dev libupsclient-dev
```

May need to update privileges
```bash
lsusb
```
Ex APC power supply - 
```bash
Bus <bus num> Device <device num>: ID <idVendor>:<idProduct> American Power Conversion Uninterruptible Power Supply
```
Set Rules
```bash
sudo vi /etc/udev/rules.d/99-nut-ups.rules
```
to:
```bash
SUBSYSTEM=="usb", ATTR{idVendor}=="<idVendor>", ATTR{idProduct}=="<idProduct>", MODE="664", GROUP="nut"
```

view of NUT 
```bash
upsc apc
```

view NUT as a web app:
```bash
docker run -e UPSD_ADDR=<host_ip> -e UPSD_USER=<nut_username> -e UPSD_PASS=<nut_pass> -p 9000:9000 ghcr.io/superioone/nut_webgui:latest
```

### Testing Power Interruptions

Controlling which battery % sends the pc shutdown signal

For testing, we can temporarily change the charge low variable (will be reset on restart by UPS) to test out when unplugged
```bash
upsrw -s battery.charge.low=90 -u <nut_username> -p <nut_pass> apc
```

view updated variable
```bash
upsc apc
```
Then unplug ups and monitor the PC when batter hits 90.  

Verify low batter again  
```bash
upsc apc
```

### Issues on re-start
- APC turns off (not just computer)
- Computer doesn't turn on automatically
- SSL/driver error with `upcs apc` on restart


fixing ssl error - 
*may need to unplug and plug usb back in*
test driver - 
```bash
sudo /lib/nut/usbhid-ups -a apc -DDD
```

```
sudo systemctl enable nut-server nut-monitor
sudo systemctl start nut-server nut-monitor
```

```
sudo upsdrvctl start
sudo systemctl restart nut-server
```

verify ups coms -  
```bash
upsc apc
```
*battery.charge.low should be back at 10*