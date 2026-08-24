Creating A Privacy Focused Remote Audio Monitor
======================================

Aug 24, 2026

![Privacy Focused Remote Audio Monitor Device](/static/img/blogs/creating-a-privacy-focused-remote-audio-monitor/sensor_side_close_small.webp)


This project addresses the challenge of capturing audio from remote nodes while prioritizing privacy. A remote monitor deployed in public capturing raw audio data with no guardrails is functionally a surveillance device. To maximize privacy and offer a lower cost DIY option to record audio, this project implements Lora for audio transfer, which does not have the bandwidth to send high quality raw audio. All of the code and files for the project are open source to further increase transparency, and to others to build their own.  

Device Running outdoors:  
![Privacy Focused Remote Audio Monitor Device Full](/static/img/blogs/creating-a-privacy-focused-remote-audio-monitor/sensor_outside_straight_close_small.webp)  


Supplemental Project Videos
----------
- [Project Context And Details](https://youtu.be/lsW-Isf31Mo)
- [Assembly walkthrough](https://youtube.com/shorts/cxjREqRgqG8?feature=share)


Software And Files
----------
- [Microcontroller code](https://github.com/PrestonBlackburn/esp32_lorawan_audio_sensor_node)
- [Chirpstack Helm Chart (server)](https://github.com/PrestonBlackburn/chirpstack-helm)
- [Chirpstack Docker (gateway)](https://github.com/xoseperez/basicstation-docker)
- [Application Helm Chart](https://github.com/PrestonBlackburn/datacenter_monitor_infra)
- [Application Code](https://github.com/PrestonBlackburn/datacenter_monitor_server)
- [3D Print Files](https://github.com/PrestonBlackburn/datacenter_monitor_case)
- [LR1302 LoRaWAN Gateway Setup](https://www.elecrow.com/wiki/lr1302-lorawan-gateway-module.html)

Background
----------
- [Data Center Infrasound Research and Education Lab](https://c3innovation.uccs.edu/data-center-infrasound-research-and-education-lab)
- [Soundscape monitoring paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12969378/pdf/main.pdf)
- [Deflock](https://maps.deflock.org)
- [LoraWan](https://www.thethingsnetwork.org/docs/lorawan/)
- [Chirpstack](https://www.chirpstack.io/)


Instructions
----------

These instructions assume you already have a high level understanding of some of the underlying tech. I'll go through some of the key pieces of the setup.
If people are interested I may put together a more in-depth walkthrough.  

High level architecture of what we are buildling:  
![High level arch](/static/img/blogs/creating-a-privacy-focused-remote-audio-monitor/high_level_arch_w_background.webp)


**The microprocessor**  
I actually started with the raspberry pi pico for this project, but I quickly found that the ESP32-S3 has much better support for a project like this and the additional processing power is nice to have. We also need some additional GPIO pins, since we are using the SX1262 Lora hat, so ESP32-S3 plus model is recommended.   
The ESP-IDF (Espressif IoT Development Framework) has some really nice features for a more complex project like this  (at least more complex than past projects I've done). I'd also recommend going through the setup and getting started guide for the [ESP-IDF cli](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/index.html)  

**Capturing Audio Data**  
We don't just want to capture the total noise levels, but the noise levels at varying frequencies. To capture audio data we'll use the Adafruit ICS-43432 breakout board. We'll capture the audio from the mic using the I2S protocol and the driver from esp-idf. The audio data is pushed to a ring buffer allows us to continuously capture audio samples. A second task processes the data in the ring buffer and applies the Short-Time Fourier Transform (STFT) to decompose the audio into a full frequency spectrum, and those are aggregated into four separate frequency bands.     
[Source Code](https://github.com/PrestonBlackburn/esp32_lorawan_audio_sensor_node/blob/main/main/esp_lorawan_mic.cpp)  


**Using Lora/Lorawan**  
Next we need to get the data back to our servers. To push data from our remote nodes to the centralized gateway we'll use Lora.  It is commonly used for off-grid communication in mesh networks like Meshtastic. While it has lower bandwidth than Cellular communication, it can also transmit data tens of miles under favorable conditions.This lower bandwidth is actually a perk for us. Lorawan has around 1000x slower data transfer rate than 5G cellular, which means it can't send high quality audio data like Cellular can.    
![bandwith v range](/static/img/blogs/creating-a-privacy-focused-remote-audio-monitor/bandwidth-vs-range.webp)
  
To equip our ESP32-S3 with lora we can use the SX1262 lora hat and the [Radiolib library](https://github.com/jgromes/RadioLib). After processing the audio data we produce an custom 11 byte message with the decibel (dBFS) measurements at four different frequency ranges. The message is in the format: version | type | length | band 0 | band 1 | band 2 | band 3 |.   

**LoraWAN Gateway and Chirpstack**  
Chirpstack is another awesome open source project that makes all of this cross-device communication possible. It helps facilitate receiving the messages, forwarding them to the server, and decoding the message. It runs on both the LoraWAN gateway and my server. I even made a custom helm chart for Chirpstack so I can manage it more easily through ArgoCD.   
![software arch](/static/img/blogs/creating-a-privacy-focused-remote-audio-monitor/software_arch_w_background.webp)   
For the gateway hardware I ended using my raspberry pi 4B with a LR1302 LoRaWAN Gateway hat, which has some pretty good docs on [Elecrow's site](https://www.elecrow.com/wiki/lr1302-lorawan-gateway-module.html)  
To run the gateway completely remotely I used a Soracom Onyx Cellular USB modem with a 1nce SIM card. This also assumes that you have a public endpoint that you can with your Chirpstack gateway, which I setup on my homelab. Since Chirpstack basicstation communicates over Websockets, Cloudflare tunnels will work. Note that the UDP packet forwarder in the Elecrow docs will not work because they communicate over layer 4, while cloudflare tunnels work best with layer 7 traffic.  
![gateway hardware](/static/img/blogs/creating-a-privacy-focused-remote-audio-monitor/lorawan_gateway_small.webp)    

- [Chirpstack Helm Chart (server)](https://github.com/PrestonBlackburn/chirpstack-helm)  
- [Chirpstack Docker (gateway)](https://github.com/xoseperez/basicstation-docker)  
- [Application Helm Chart](https://github.com/PrestonBlackburn/datacenter_monitor_infra)    
- [Application Code](https://github.com/PrestonBlackburn/datacenter_monitor_server)   

**Solar Setup**  
The solar setup is pretty standard. I use the waveshare solar power manager module with two 18650 batteries and a 10W 12V solar panel. It could potentially use a larger solar panel and more batteries to last a little longer, but I haven't had any issues in the testing I've done so far.   

**3D Printable Case**  
The last piece of this project was the 3D printed case. The main goal of the case was to just keep the components dry and provide a standoff for the mic. I think it turned out well for my first real FreeCAD project, but I'm sure there are a lot of improvements that could be made.   


[3D Print Files](https://github.com/PrestonBlackburn/datacenter_monitor_case)  

**Final Hardware Setup**  
![hardware arch](/static/img/blogs/creating-a-privacy-focused-remote-audio-monitor/hardware_arch_w_background.webp)  



Bill Of Materials
----------
**Sensor**  
Seeed Studio XIAO ESP32-S3 Plus  
Wio-SX1262 for XIAO  
Mic (audio sensor) - Adafruit I2S MEMS Microphone Breakout - ICS-43434  
2x 18650 Batteries - Panasonic NCR18650GA (Sanyo GA) 18650 3450mAh 10A Battery  
2x Battery holders  
Waveshare Solar Power Manager Module (D)  - Supports 6V~24V Solar Panel and Type-C Power Adapter, 5V/3A Regulated Output  
2.6dBi Long Range Antenna - SMA male - 915MHz - 195mm  
SMA to I-PEX Antenna Cable - 120mm  
Microphone Pop Filters  
M2 screws for 3d printed case  
USB C cables  
12V 10W Monocrystalline Solar Panel  
(optional - long range applications) - 6 dBi Low Profile N-Female Omni Outdoor 915 MHz Antenna for Helium RAK Miner Bobcat & Meshtastic  
(optional - long range applications) - UFL(IPEX/IPX) Mini PCI to N-MALE Pigtail Cable Extension - 8" (1.13 shielding)  
(optional - long range applications) - Rokland RokTape- Waterproof Tape for Helium or WiFi Antennas & Coaxial Cables 1 Roll 15 ft. - Self Fusing Silicone  

**Gateway**  
LR1302 LoRaWAN Gateway Module SPI US915 SX1302 Long Range Gateway Module Support 8 Channels  
Raspberry Pi 5 2GB (need to test - might be able to get away with less RAM)  
(optional - long range applications) ALFA Network 12 dBi N-Female Directional Yagi  
(optional -  long range applications) 3 ft. Antenna extension coaxial cable RP-SMA male to N-male RFC-400 low loss  
(optional - remote gateway applications) - Soracom Onyx LTE USB Modem  
(optional - remote gateway applications) - IoT data SIM card - ex: 1nce  
(optional - remote gateway applications) - 90 amp hr Battery, 12V  
(optional - remote gateway applications) - Weather proof case -  10.2"x6.3"x3.9"  
(optional - remote gateway applications) - 50W solar panel, 12V  
(optional - remote gateway applications) - Solar charge controller - ex: Renogy Wanderer  

**Peripherals**  
10ft fence post  
Fence post brackets  
1/2 Plywood for mounting  

**Tools**  
3d Printer  
Fine-tipped Solder Iron  