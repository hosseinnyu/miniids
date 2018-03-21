# Intro

This is a simple but elegant IDS. For now, it only works with HTTP traffic.

# Architecture

The architecture of the SemanIDS is layered based. Higher leyers plug (equal to the concept of subscribe) to a lower layer, and lower layers notify higher levels of the events.


|-----------------------------------------------------------------------------------|  
|..........................................Monitor................................................|  
|-----------------------------------------------------------------------------------|  
|..........................................IDS.............|...............Rules................|  
|-----------------------------------------------------------------------------------|  
|..........................................Analyzers.............................................|  
|-----------------------------------------------------------------------------------|  
|..........................................Consumers............................................|  
|-----------------------------------------------------------------------------------|  
|..........................................Sensors...............................................|  
|-----------------------------------------------------------------------------------|  

## Description of Layers

* Sensors: Sniffers the listen to traffics on an interfaces (e.g., using scapy) and notify the plugged consumers per recieved packet.

* Consumers: Classes that get packets from the sensors (i.e., get notified) and extract the interesting fields. The consumers keep a buffer of data of interests. This buffer can be size and timelimited (i.e., packets may expire)

* Analyzer: Analyzers do statistical analysis on the packets. An analyzer plugs to a consumer and is able to read the buffers. The analysis can be a simple word-count to more complicated anlaysis. 

* Dashboard: each analysis function over a target data of interest installs itself into a dashboard of "meters" and can be accessed by ids layer. I call each items in the dashboard a meter (similar to meters in real word).

* IDS: is the layer where the rules are checked against the meters and alerts or notifications are generated. For example, if count of the recently visited websites in above a given threshold, then this can create an alert.

* Monitor: is basically the boot engine where the configuration of a running IDS is defined, objects are created, and layers are created and plugged on top of each other.

* Terminaloutput: is a class that helps to have a decent output system with several sections (in this case on for alerts and one for notification), that makes the monitoring of the system very easy.

In order to run this on your machine, you need to modify the file sensor, line 29, and put the name of the interface you wan to sniff. Then, run:
sudo python monitor.py





