# knobsChanger
Nuke tool that changes same parameter on a selection of nodes

This is an improved version of the knobsChanger. It now works with most of the knobs available in a Nuke Panel. 
The UI is, in most cases, the same as the soruce knob. 
I've also added the option to update to UI as we tweak the values.

Instrucctions:

When working with large scripts you usually end up having to change the same knob (parameter) 
in a range of nodes through out the script until achieving the best result. Eg: filters, shutters,... 

I always missed having a tool that allowed me to selected those nodes, say which common parameter 
I wanted to change and set my change on all of them at once.

So that is how it works. We select the nodes to change, they don't need to be the same kind of node, 
just have a common knob. Then you execute the tool and need to enter the python name of the knob to change. 
You can find it my placing the mouse cursor on top of knob.
