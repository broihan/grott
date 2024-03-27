import datetime
import os
import json
import paho.mqtt.publish as publish

def grottext(conf, data, jsonmsg) :
    """
    Grot extension to write to MQTT topic that is consumed by "dbus_mqtt_pv" Venus OS driver to integrate arbitrary pv inverter into Venus OS.
    Version 0.0.1
    Date 26.03.2024
    """

    resultcode = 0

    if conf.verbose :

        print("\t - " + "Grott extension module grott_dbus_mqtt_inverter entered")
        print("\t\tMQTT-IP: " + conf.mqttip)
        
    jsonobj = json.loads(jsonmsg)
    
    output = {}
    output['pv'] = {}
    output['pv']['power'] = jsonobj['values']['pvpowerout']/10
    output['pv']['energy_forward'] = jsonobj['values']['pvenergytotal']/10
    output['pv']['voltage'] = (jsonobj['values']['pvgridvoltage']/10 + jsonobj['values']['pvgridvoltage']/10 + jsonobj['values']['pvgridvoltage']/10) / 3
    output['pv']['current'] = jsonobj['values']['pvgridcurrent']/10 + jsonobj['values']['pvgridcurrent2']/10 + jsonobj['values']['pvgridcurrent3']/10
    output['pv']['L1']={}
    output['pv']['L2']={}
    output['pv']['L3']={}
    output['pv']['L1']['power'] = jsonobj['values']['pvgridpower']/10
    output['pv']['L2']['power'] = jsonobj['values']['pvgridpower2']/10
    output['pv']['L3']['power'] = jsonobj['values']['pvgridpower3']/10
    output['pv']['L1']['current'] = jsonobj['values']['pvgridcurrent']/10
    output['pv']['L2']['current'] = jsonobj['values']['pvgridcurrent2']/10
    output['pv']['L3']['current'] = jsonobj['values']['pvgridcurrent3']/10
    output['pv']['L1']['voltage'] = jsonobj['values']['pvgridvoltage']/10
    output['pv']['L2']['voltage'] = jsonobj['values']['pvgridvoltage2']/10
    output['pv']['L3']['voltage'] = jsonobj['values']['pvgridvoltage3']/10
    output['pv']['L1']['frequency'] = jsonobj['values']['pvfrequentie']/100
    output['pv']['L2']['frequency'] = jsonobj['values']['pvfrequentie']/100
    output['pv']['L3']['frequency'] = jsonobj['values']['pvfrequentie']/100
    
    if conf.verbose : 
        print("\t\tPayload: " + json.dumps(output))
        
    publish.single("enphase/envoy-s/meters", payload=json.dumps(output), hostname=conf.mqttip)
    

    return resultcode
