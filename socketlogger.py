#
#    Copyright (c) 2012 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
#    $Revision: 1 $
#    $Author: pobrien $
#    $Date: 2016-01-14 08:00:00 -0500 (Thu, 14 Jan 2016) $
#
""" This driver connects to a socket (typically on localhost) and waits 
    for packet data. Once a new line comes into the socket, this will process
    the data and submit the packet back to weewx. 
    
    Based on the hackulink driver, which was based on the weewx wmr100 driver
"""

import socket
import syslog
import time

import weedb
import weewx.drivers
import weeutil.weeutil
import weewx.wxformulas

def logmsg(dst, msg):
    syslog.syslog(dst, 'SocketLogger: %s' % msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)
    
def logerror(msg):
    logmsg(syslog.LOG_ERROR, msg)
    
def logdebug(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loader(config_dict, engine):
    station = SocketLogger(**config_dict['SocketLogger'])
    return station
        
class SocketLogger(weewx.drivers.AbstractDevice):
    """ Driver for the SocketLogger station. """
    
    def __init__(self, **stn_dict) :
        """ Initialize an object of type SocketLogger. """
        
        self.host_ip          = stn_dict.get('host_ip')
        self.host_port        = int(stn_dict.get('host_port'))
        self.timeout          = float(stn_dict.get('timeout'))
        self.station_hardware = stn_dict.get('hardware')
        
        self.lastrain = None

        self.port = None
        self.openPort()

    def hardware_name(self):
        return self.station_hardware
    
    def openPort(self):
        try:
            loginf("Connecting to socket on %s port %s" % (self.host_ip, self.host_port) )
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect( (self.host_ip, self.host_port) )
        except (socket.error, socket.timeout, socket.herror), ex:
            logerror("Socket error while opening port %d to ethernet host %s." % (self.host_port, self.host_ip))
            # Reraise as a weewx I/O error:
            raise weewx.WeeWxIOError(ex)
        except:
            logerror("Unable to connect to host %s on port %d." % (self.host_ip, self.host_port))
            raise
        logdebug("Connected to host %s on port %d" % (self.host_ip, self.host_port))
        self.port = self.socket.makefile()
        
    def closePort(self):
        self.port.close()
                
    def check_rain(self, daily_rain_counter):
        # *** DO NOT use the &rainin= data! ***
        # Handle the rain accum by taking the &dailyrainin= reading ONLY.
        # Then submit those minor increments of daily rain to weewx.
        rain = 0.0
        current_rain = float(daily_rain_counter)
        if self.lastrain is not None:
            if (current_rain >= self.lastrain):
                rain = float(current_rain) - float(self.lastrain)
                #loginf("Checking for new rain accumulation")
                #loginf(rain)
        self.lastrain = current_rain
        return rain
        
    #===============================================================================
    #                         LOOP record decoding functions
    #===============================================================================

    def genLoopPackets(self):
        """ Generator function that continuously returns loop packets """
        for _packet in self.genPackets():
            yield _packet
                
    def genPackets(self):
        """ Generate measurement packets from the socket. """
        while True:
            try:
                _line = self.port.readline(4096)
                #loginf(_line)
            except (socket.timeout, socket.error), ex:
                raise weewx.WeeWxIOError(ex)
            if _line == None:
                break
            else:
            #if _line[0:8] == 'outTemp=':
                #loginf("New data received on socket.")
                yield self._process_message(_line)
    
    def _process_message(self, message):
        _packet = {}

        #separate line into a dict
        message = message.rstrip() # Strip any newline
        line = message.split(',') # Split by comma
        data = dict( [ i.split( '=' ) for i in line] ) # Create dictionary of the values
        
        _packet['dateTime'] = int(time.time())
        _packet['usUnits'] = weewx.US
        _packet['outTemp'] = float( data["outTemp"] )
        _packet['outHumidity'] = float( data["outHumidity"] )
        _packet['inTemp'] = float( data["inTemp"] )
        _packet['inHumidity'] = float( data["inHumidity"] )
        _packet['barometer'] = float( data["barometer"] )
        _packet['rain'] = self.check_rain( data["dailyrain"] )
        _packet['windDir'] = float( data["windDir"] )
        _packet['windSpeed'] = float( data["windSpeed"] )
        _packet['windGust'] = float( data["windGust"] )
        _packet['radiation'] = float( data["radiation"] )
        _packet['UV'] = float( data["UV"] )
        _packet['txBatteryStatus'] = float( data["txBatteryStatus"] )
        #loginf(_packet)
        return _packet
