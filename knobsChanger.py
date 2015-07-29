
par = [] # this will remember the last entry, keep it out of the funcion

class knobsChanger( nukescripts.PythonPanel ):
    def __init__(self, k, paramName):
        nukescripts.PythonPanel.__init__( self, "test")

        knobT = getattr(nuke,k)
        self.knob = knobT(paramName)
        self.addKnob(self.knob)

    def showModalDialog(self):
        nukescripts.PythonPanel.showModalDialog(self)

        return self.knob.value()

def changer():
    
        nodes = nuke.selectedNodes()
        
        if nodes:  
            # this if statement remembers the last entry, using par variable out of function
            if par != []:
                param = nuke.getInput('Parameter to change', ' '.join(par))
                if param == None:
                    pass
                else:
                    par.pop()
                    par.append(param)
            else:
                param = nuke.getInput('Parameter to change', '')
                par.append(param)
                if param == None:
                    par.pop()
            
        paramObject = nuke.selectedNode().knob('%s' %param)
        paramName = paramObject.name()
        paramClass = paramObject.Class()
        paramValue = paramObject.value()
        #paramValues = paramObject.values()

        result = knobsChanger(paramClass,paramName).showModalDialog()

        for node in nodes:
            try:
                node[paramName].setValue(result)
            except:
                pass
  
# got to fix mask, enumeration knobs and pulldowns and has

