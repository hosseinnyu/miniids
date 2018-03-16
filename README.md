# Intro

This is a simple but elegant IDS. For now, it only works with HTTP traffic.

#Architecture

The architecture of the SemanIDS is layered based. Higher leyers plug (equal to the concept of subscribe) to a lower layer, and lower layers notify higher levels of the events.


|-----------------------------------------------------------------------------------|
|                                Monitor                                            |
|-----------------------------------------------------------------------------------|
|                                  IDS           |             Rules                |
|-----------------------------------------------------------------------------------|
|                              	 Analyzers                                          |
|-----------------------------------------------------------------------------------|
|                                Consumers                                          |
|-----------------------------------------------------------------------------------|
|                                Sensors                                            |
|-----------------------------------------------------------------------------------|









