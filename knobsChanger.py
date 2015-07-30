
par = [] # this will remember the last entry, keep it out of the funcion

class knobsChanger( nukescripts.PythonPanel ):
    def __init__(self, knobClass, knobName, knobObject):
        nukescripts.PythonPanel.__init__( self, "test")

        knobT = getattr(nuke,knobClass)

        if knobClass in ('Enumeration_Knob', 'Pulldown_Knob'):
            enumValues = knobObject.values()
            self.knob = knobT(knobName, knobName, enumValues)
        else:
            self.knob = knobT(knobName)
        self.addKnob(self.knob)

    def showModalDialog(self):
        nukescripts.PythonPanel.showModalDialog(self)

        return self.knob.value()

def changer():
    
        nodes = nuke.selectedNodes()
        
        if nodes:  
            # this if statement remembers the last entry, using par variable out of function
            if par != []:
                knob = nuke.getInput('Parameter to change', ' '.join(par))
                if knob == None:
                    pass
                else:
                    par.pop()
                    par.append(knob)
            else:
                knob = nuke.getInput('Parameter to change', '')
                par.append(knob)
                if knob == None:
                    par.pop()
            
        knobObject = nuke.selectedNode().knob('%s' %knob)
        knobName = knobObject.name()
        knobClass = knobObject.Class()
        knobValue = knobObject.value()
        #knobValues = knobObject.values()

        result = knobsChanger(knobClass,knobName,knobObject).showModalDialog()

        for node in nodes:
            try:
                node[knobName].setValue(result)
            except:
                pass
  
# got to fix mask, enumeration knobs and pulldowns and has

