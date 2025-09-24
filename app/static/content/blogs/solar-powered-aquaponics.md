Solar Powered Aquaponics System With Monitoring
================================================

May 29, 2022

![Ice Pick Logo](/static/img/blogs/solar-powered-aquaponics/aqua_card_photo.webp)

##  Part 1: Initial Setup

Over the last year, I haven’t been eating fish in part due to the in-sustainability of commercial fishing and farming; however, I still want to eat fish that are raised in a more sustainable way, so I turned to aquaponics. Overfishing is still very prevalent despite the rise in farmed fish ([Overfishing Data](https://ourworldindata.org/fish-and-overfishing#how-much-of-the-world-s-fish-is-managed-sustainably)). Furthermore, commercial fishing gear makes up a substantial percentage of the waste in the ocean, around 10% ([FAO Fisheries and Aquaculture Technical Paper No. 523](https://www.fao.org/3/i0620e/i0620e02.pdf)).

While farmed fish may seem like a good alternative to wild-caught fish, many times farmed fish are fed wild-caught fish. This context inspired me to create my own aquaponics system.  
*Also, see initiatives by MarViva for marine governance — https://marviva.net/en/*

A goal of this project is to try and raise fish and plants in a more sustainable way through aquaponics. Apart from raising fish, aquaponics is much more water-efficient than soil farming techniques and can produce greater yields per area. Some studies claim that aquaponics can achieve over 95% water efficiency compared to soil methods ([Recirculating aquaculture systems](https://doi.org/10.1016/j.aquaeng.2012.11.008)). Another goal of the project is to document my findings and provide resources to anyone else who might be interested in setting up a similar system.

This pilot project will help me test and monitor different approaches and assess the sustainability of the system before I scale it up. Since this system will be completely standalone, I will be using solar to power all electronics. For detailed monitoring and assessment, I’m using a Raspberry Pi to control various sensors, and I’m sending the data to AWS. Once I have the data in AWS, I’ll serve it to an app where I can monitor the system’s performance, and I’ll be able to model the future performance with machine learning.

For the first part of this project, I set up and tested the key components of the system. The key components that need to be set up are the solar system, plumbing, and monitoring. For each of these components, I’ll provide instructions or links for their setup and links to where to buy the elements of each component.  

---

## Part 1 Scope
- Solar setup — Verify the solar setup can run the pump and Raspberry Pi  
- Plumbing setup — Verify the plumbing setup can continuously fill and drain  
- Monitoring setup — Verify that Raspberry Pi can run on the solar system and send data to the cloud db  

---

## Solar Setup
For the solar setup, we will basically need to create a solar-powered outlet. The most difficult part of setting up this system is making sure all of the elements of the system are compatible with each other. As long as all of the components are compatible, it is just a matter of wiring everything together.

A diagram of my setup is shown below. At the bottom of this post, you can find all of the Amazon links to these components.

![Solar system setup](/static/img/blogs/solar-powered-aquaponics/solar_system.webp)

*A note on wiring the components — Always make sure the battery is connected to the controller before connecting the solar panel. Always take care when handling electronics.*

**Main Elements**
1. **Solar panel**  
   a. Provides system with power  
   b. As soon as the sun hits the panel it is live, so take necessary precautions  

2. **Solar controller**  
   a. Makes sure the battery isn’t overcharged and provides other safety features  

3. **Battery**  
   a. Use a deep cycle battery (normal batteries only provide short bursts, deep cycle can provide steady power)  
   b. Store power for when the sun isn’t out (3 days is a good target)  

4. **Fuse**  
   a. Breaks the circuit if current goes over 10 Amps, protecting the controller  
   b. Manufacturer recommended  

5. **12 gauge wire**  
   a. Thick enough to transfer the needed power  

**Findings**  
1. Worked as expected  
2. Waterproofing may be a challenge  
3. The inverter and battery put off heat  
4. Batteries will be the most expensive part  
5. Next steps: look into panel and battery sizing to ensure the system runs a few days without sun  

---

## Plumbing Setup
For the plumbing setup, we need to make the reservoir, grow bed, and bell siphon. The bell siphon will drain the grow bed once the water reaches a specific level. The pump moves the water up from the reservoir to the grow bed.

![Plumbing system setup](/static/img/blogs/solar-powered-aquaponics/pumbing_system.webp)  

**Main Elements**
1. **Bell Siphon**  
   a. Drains the bed completely when water reaches a certain level  
   b. Trial and error to get it working properly  
   c. [YouTube Setup Video](https://www.youtube.com/watch?v=Ia1BQFTaG7c)  
   d. [In-depth paper on bell siphons](https://www.ctahr.hawaii.edu/oc/freepubs/pdf/bio-10.pdf)  

2. **Clay ball grow bed**  
   a. Provides a medium for plants to grow  
   b. Must be inert for aquaponics so it doesn’t affect water quality/fish  

3. **Pump**  
   a. Water should be circulated 1–3 times/hour (e.g., 50 gallon system needs 50–150 gph pump)  
   b. My pump had too high of a flow rate, smaller would work fine  

**Findings**  
1. Had trouble getting the siphon to work, still troubleshooting  
2. Debris built up quickly, will need covering and potentially a filter  

---

## Monitoring Setup
For the monitoring setup, I’ll use a Raspberry Pi with sensors to take measurements, and send/store them in AWS. This will let me monitor the system in real-time.  

We’ll need to:  
- Create a script to collect/send data  
- Enable remote connection to Raspberry Pi  
- Set up a serverless API + DB in AWS  

**Main Elements**
1. **Raspberry Pi 4 Setup**  
   - [Video Overview](https://www.youtube.com/watch?v=jRKgEXiMtns&t=621s)  

2. **Collecting Data (DHT 22 Sensor)**  
   - Use `Adafruit-circuitpython-dht` library  
   - [Setup Video](https://www.youtube.com/watch?v=EcyuKni3ZTo)  
   - [Setup Blog](https://www.piddlerintheroot.com/dht22/)  

3. **Remote Connection (SSH)**  
   - [SSH Setup Guide](https://libguides.nyit.edu/c.php?g=469894&p=3365470)  
   - Issue: Pi wouldn’t connect unless monitor was plugged in → reflashing OS fixed it  
   - Ping the Pi’s IP to verify it’s online  

4. **Serverless API**  
   - [AWS API Setup with Python](https://libguides.nyit.edu/c.php?g=469894&p=3365470)  
   - [AWS API Setup with JavaScript](https://libguides.nyit.edu/c.php?g=469894&p=3365470)  
   - Use API Gateway (MQTT preferred, will explore later)  

**Findings**  
- Raspberry Pi inconsistently sent data  
- Unevenly spaced measurements in DB → possible Wi-Fi issues, needs further investigation  

![Sensor results](/static/img/blogs/solar-powered-aquaponics/sensor_results.webp)  

---

## System Pictures
![System card](/static/img/blogs/solar-powered-aquaponics/aqua_card_photo.webp)  
![Reservoir](/static/img/blogs/solar-powered-aquaponics/reservoir_side.webp)  
![Bell siphon](/static/img/blogs/solar-powered-aquaponics/bell_siphon.webp)    
![Waterproofing](/static/img/blogs/solar-powered-aquaponics/waterproofing.webp)   

---

## Product List
**Solar**  
- [Panel](https://www.amazon.com/gp/product/B01LY02BOA/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)  
- [Panel Brackets](https://www.amazon.com/gp/product/B08HLH58L1/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1)  
- [Solar to wire connectors](https://www.amazon.com/gp/product/B00DGXGKWA/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)  
- [Controller](https://www.amazon.com/gp/product/B07NPDWZJ7/ref=ppx_yo_dt_b_asin_title_o01_s01?ie=UTF8&psc=1)  
- [Inverter](https://www.amazon.com/gp/product/B07RSB6PMN/ref=ppx_yo_dt_b_asin_title_o01_s01?ie=UTF8&psc=1)  
- [Battery](https://www.amazon.com/gp/product/B00K8E0WAG/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1)  
- [Fuse](https://www.amazon.com/gp/product/B07RY8Y2QV/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)  
- [12 Gauge quick disconnect](https://www.amazon.com/gp/product/B081VDY95P/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)  

**Plumbing**  
- [Pump](https://www.amazon.com/gp/product/B07L54HB83/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1)  
- [55 gal reservoir tote](https://www.homedepot.com/p/HDX-55-Gal-Tough-Storage-Tote-in-Black-with-Yellow-Lid-HDX55GONLINE-4/205597365)  
- [68 Qt media bed tote](https://www.cabelas.com/shop/en/plano-medium-storage-trunk?rrec=true)  
- [Bulkhead fitting](https://www.amazon.com/gp/product/B07XRGNXWL/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)  
- [¾ in PVC adaptor](https://www.amazon.com/gp/product/B092SGM2KZ/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)  
- [Clay Pebbles](https://www.amazon.com/gp/product/B009LNOZQ2/ref=ppx_yo_dt_b_asin_title_o06_s02?ie=UTF8&psc=1)  
- [PVC](https://www.homedepot.com/s/pvc?NCNI-5) — ¾ in, 4 in, 2 in  
- [PEX](https://www.homedepot.com/s/pex?NCNI-5) — ½ in (recommend PVC/tubing instead unless you’re familiar)  
- [Ball valve](https://www.homedepot.com/s/pex%2520ball%2520valve?NCNI-5) (to control flow to media bed)  

**Monitoring**  
- [Raspberry Pi Kit](https://www.raspberrypi.com/products/raspberry-pi-4-desktop-kit/)  
- [DHT 22 Sensor](https://www.amazon.com/Gowoops-Temperature-Humidity-Measurement-Raspberry/dp/B073F472JL)  

---

## Further Future Improvements
**Solar**  
- Add additional batteries  
- Improve waterproofing  

**Plumbing**  
- Improve bell siphon  

**Monitoring**  
- Add additional sensors  
- Investigate API inconsistencies  
- Heat sink for Raspberry Pi (very hot after 12 hrs outside)  
- Independent power supply  

---