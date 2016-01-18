# weewx SocketLogger driver

Inspired from the hackulink driver, which was based on the weewx wmr100 driver, this weewx driver will connect to a socket server and listen for weather data. The weather data needs to be comma separated and contain a sensor schema that matches the database.

My specific use case to make this drive is that I own the Ambient Weather WS-1200-IP and there is no way to redirect the weather data to your own server. So I came up with a TCP iptables redirect that gets the data into weewx using PHP and ncat as a socket server. Once weewx has the data, then you can have weewx update CWOP, PWSWeather, WeatherBug and more. 

This driver requires:
- Installing a socket server (ncat is what I used)

## Install
- Copy the socketlogger.py driver to the `bin/user` folder (For my CentOS install it's located at `/usr/share/weewx/user`)
- Copy the text blurb from the `weewx.conf` here to your `weewx.conf`
- Modify the configuration in `weewx.conf` to update the IP and hardware description
- Restart weewx

## Version
1.0 - Initial

## Warranty

There is no warranty that this will work. In my testing it seems very stable, but admittedly there could be a few bugs that I haven't come across yet. Note, if the socket server crashes or if weewx crashes, then no data is being captured, which means your data is not being logged and you're not updating any weather services. 

I'm open to pull requests to make this better!
