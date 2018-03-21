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

* Dashboard: Analyzers install themselves into a dashboard and announce themselves as a "meter" each. The meters are usually accessed by IDS layer. These meters are basically the data points that IDS observes from the network behaviors.

* IDS: IDS layer includes the logic and rules of creating alerts based on the observed network behaviors. At the moment, rules are hard-coded into this module. Ideally, there will be a rule definition language that describes when to generate an alert. IDS pulls the data points from the dashboard, that in turned is bound to the analyzers. The IDS layer notfies a subscriber when an alert or notifcation is created.

* Monitor: Is the initialization and run engine where the layers are created and configured, and layers are plugged on top of each other. 

* Terminaloutput: Is bascially the UI class that shows notifications and alerts. It constantly refreshes the screens and shows different sections accordingly.

## How to run?
To run the IDS on your machine, you need to first modify the sensor.py file and put the name of the interface on your machine to sniff. Then, run:

sudo python monitor.py





