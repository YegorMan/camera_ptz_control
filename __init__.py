import sys
import time
import requests

DOMAIN = 'camera_ptz_control'
ACTION = 'move'

IP_NAME = 'ip'
PAN_NAME = 'pan'
TILT_NAME = 'tilt'
TIMEOUT_NAME = 'timeout'

PAN_DEFAULT_VALUE = '0'
TILT_DEFAULT_VALUE = '0'
TIMEOUT_DEFAULT_VALUE = '0'

def setup(hass, config):
    def perform_action(address, pan, tilt):
        url = 'http://{}:8899/onvif/ptz'.format(address)
        headers = {'content-type': 'application/soap+xml'}
        body = """<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"><s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><ContinuousMove xmlns="http://www.onvif.org/ver20/ptz/wsdl"><ProfileToken>stream0_0</ProfileToken><Velocity><PanTilt x="{}" y="{}" xmlns="http://www.onvif.org/ver10/schema"/></Velocity></ContinuousMove></s:Body></s:Envelope>""".format(pan, tilt)
        requests.post(url, data=body, headers=headers)

    def stop_action(address):
        url = 'http://{}:8899/onvif/ptz'.format(address)
        headers = {'content-type': 'application/soap+xml'}
        body = """<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"><s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><Stop xmlns="http://www.onvif.org/ver20/ptz/wsdl"><ProfileToken>stream0_0</ProfileToken><PanTilt>true</PanTilt><Zoom>false</Zoom></Stop></s:Body></s:Envelope>"""
        requests.post(url, data=body, headers=headers)

    def handle_camera_ptz_control(call):
        ip = call.data.get(IP_NAME)
        pan = call.data.get(PAN_NAME, PAN_DEFAULT_VALUE)
        tilt = call.data.get(TILT_NAME, TILT_DEFAULT_VALUE)
        timeout_str = call.data.get(TIMEOUT_NAME)

        hass.states.set('camera_ptz_control.name', 'yegorman')

        perform_action(ip, pan, tilt)

        if timeout_str is not None:
            timeout = float(timeout_str)
            time.sleep(timeout)
            stop_action(ip)

    hass.services.register(DOMAIN, DOMAIN, handle_camera_ptz_control)

    return True
    
