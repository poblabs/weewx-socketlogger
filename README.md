# weewx SocketLogger driver

Inspired from the hackulink driver, which was based on the weewx wmr100 driver, this weewx driver will connect to a socket server and listen for weather data. The weather data needs to be comma separated and contain a sensor schema that matches the database.

My specific use case to make this driver is that I own the Ambient Weather WS-1200-IP and there is no way to redirect the weather data to your own server. So I came up with a TCP iptables redirect that gets the data into weewx using PHP and ncat as a socket server. Once weewx has the data, then you can have weewx update CWOP, PWSWeather, WeatherBug and more. 

For the writeup on how I'm using this driver with the weather station data iptables redirect and a socket server, check it out here on my blog: http://obrienlabs.net/redirecting-weather-station-data-from-the-ambient-weather-observerip/

This driver requires:
- A socket server (ncat is what I used)
  - If you don't want to use ncat, the Python socket library could be hooked in pretty easily I would think. However, this would make the socket available only when weewx is running. This may not be ideal for all situations. 

## Install
- Copy the socketlogger.py driver to the `bin/user` folder (On CentOS and Ubuntu install it's located at `/usr/share/weewx/user`)
- Copy the text snippet from the `weewx.conf` in this repo to your `weewx.conf`
- Modify the configuration in `weewx.conf` to update the IP and port information for the socket server, also update the hardware description if needed
- Restart weewx

## Version
1.0 - Initial

## Troubleshooting
- The driver contains many commented log points as `loginf()`. Uncomment one, restart weewx and keep an eye on the log file to see if it can offer insight on what's wrong. 

## Warranty

There is no warranty that this will work. In my testing it seems very stable, but admittedly there could be a few bugs that I haven't come across yet. Note, if the socket server crashes or if weewx crashes, then no data is being captured, which means your data is not being logged and you're not updating any weather services. 

I'm open to pull requests to make this better!
