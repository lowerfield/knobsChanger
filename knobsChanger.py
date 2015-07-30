
par = [] # this will remember the last entry, keep it out of the funcion

class KnobsChanger(nukescripts.PythonPanel):

    def __init__(self, knobClass, knobName, knobObject):
        nukescripts.PythonPanel.__init__( self, "Parameter Changer")

        knobToChange = getattr(nuke,knobClass)

        if knobClass in ('Enumeration_Knob', 'Pulldown_Knob'):
            enumValues = knobObject.values()
            self.knob = knobToChange(knobName, knobName, enumValues)
        else:
            self.knob = knobToChange(knobName)
           
        self.addKnob(self.knob)
         
        self.exprCheck = nuke.Boolean_Knob('Set expression')
        self.exprCheck.clearFlag(nuke.STARTLINE)
        self.expr = nuke.EvalString_Knob('=')
        self.expr.setVisible(False)
        self.addKnob(self.exprCheck)
        self.addKnob(self.expr)

    def knobChanged(self, knob):
        
        if self.exprCheck.value() == True:
            self.expr.setVisible(True)
        else:
            self.expr.setVisible(False)

    def showModalDialog(self):
        nukescripts.PythonPanel.showModalDialog(self)

        return self.knob.value(), self.expr.value()

def knobsChanger():
    
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
        
        for node in nodes:   

            if node['%s'%knob] == 'NoneType':
                pass

            else:
                knobObject = node['%s'%knob]
                break

        knobName = knobObject.name()
        knobClass = knobObject.Class()
        knobValue = knobObject.value()

        if knobObject != 'NoneType':
            result = KnobsChanger(knobClass,knobName,knobObject).showModalDialog()

        else:
            nuke.message("Knob does not exist")
            return

        for node in nodes:

            try:
                if result[1] != '':
                    node[knobName].setExpression(result[1])
                else:
                    node[knobName].clearAnimated()
                    node[knobName].setValue(result[0])
                    
            except:
                pass
  