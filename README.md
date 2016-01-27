# PoC of loosely coupled MANO framework

## Requirements
* Running RabbitMQ broker instance on local machine
* Python Pika: `sudo pip install pika`


## Folder structure:
* kernelpoc/
	* sonbase/ Abstract plugin class to simplify implementation of other plugins
	* sonpluginmanager/ Main plugin, to which other plugins register. Bookkeeping etc.
	* plugin1/ Simple example plugin
	* sonlog/ Plugin that prints every message sent over the broker
	* sonplacement/ Placement plugins dummy
	* sonconflict/ Conflict resolution dummy
	* sonlifecycle/ Lifecycle management dummy


## Example A: Simple plugin registration

Run the following commands (each in an own terminal = 2 terminals):
* `python -m kernelpoc.sonpluginmanager`
* `python -m kernelpoc.plugin1`

## Example B: Complex workflow using multiple plugins

Run the following commands (each in an own terminal = 6 terminals):

* `python -m kernelpoc.sonpluginmanager`
* `python -m kernelpoc.sonlog`
* `python -m kernelpoc.sonplacement`
* `python -m kernelpoc.sonconflict`
* `python -m kernelpoc.sonlifecycle`
* `python -m kernelpoc.plugin1`
