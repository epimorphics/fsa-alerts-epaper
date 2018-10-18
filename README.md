# FSA Alerts E-paper Demo

Displays latest food alert on Waveshare 4.2Inch e-Paper module (B) with a raspberry pi zero w

# Setup

Follow the [module setup guide](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_(B)#Working_with_Raspberry_Pi)

Then run the code with 

```
python main.py
```

# Running long term

We are running this code with a systemd unit so that it runs as soon as the pi is plugged in and has booted up.

```
[Unit]
Description=Food alerts agent
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/fsa-alerts-epaper
ExecStart=/usr/bin/python /home/pi/fsa-alerts-epaper/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```
