
par = [] # this will remember the last entry, keep it out of the funcion

class knobsChanger(nukescripts.PythonPanel):

    def __init__(self, knobClass, knobName, knobObject):
        nukescripts.PythonPanel.__init__( self, "test")

        knobT = getattr(nuke,knobClass)

        if knobClass in ('Enumeration_Knob', 'Pulldown_Knob'):
            enumValues = knobObject.values()
            self.knob = knobT(knobName, knobName, enumValues)
        else:
            self.knob = knobT(knobName)
           
        self.addKnob(self.knob)
         
        self.exprCheck = nuke.Boolean_Knob('Set expression')
        self.exprCheck.clearFlag(nuke.STARTLINE)
        self.addKnob(self.exprCheck)

        self.expr = nuke.EvalString_Knob('=')
        self.expr.setVisible(False)
        self.addKnob(self.expr)

    def knobChanged(self, knob):
        
        if self.exprCheck.value() == True:
            self.expr.setVisible(True)
        else:
            self.expr.setVisible(False)

    def showModalDialog(self):
        nukescripts.PythonPanel.showModalDialog(self)

        return self.knob.value(),  self.expr.value()

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

        result = knobsChanger(knobClass,knobName,knobObject).showModalDialog()

        for node in nodes:
            try:
                node[knobName].setValue(result[0])
                if result[1] != '':
                    node[knobName].setExpression(result[1])
                else:
                    pass
            except:
                pass
  
# got to fix mask
