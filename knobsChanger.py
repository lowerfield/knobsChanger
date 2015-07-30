
par = [] # this will remember the last entry, keep it out of the funcion

class KnobsChanger(nukescripts.PythonPanel):

    def __init__(self, knobClass, knobName, knobObject, nodes):
        nukescripts.PythonPanel.__init__( self, "Parameter Changer")

        self.knobObject = knobObject
        self.nodes = nodes
        self.knobName = knobName

        knobToChange = getattr(nuke,knobClass)


        if knobClass in ('Enumeration_Knob', 'Pulldown_Knob'):
            enumValues = self.knobObject.values()
            self.knob = knobToChange(knobName, knobName, enumValues)
        else:
            self.knob = knobToChange(knobName)
           
        self.addKnob(self.knob)
        self.knob.setValue(knobObject.value())
         
        self.exprCheck = nuke.Boolean_Knob('Set expression')
        self.exprCheck.clearFlag(nuke.STARTLINE)
        self.expr = nuke.EvalString_Knob('=')
        self.expr.setVisible(False)
        self.addKnob(self.exprCheck)
        self.addKnob(self.expr)

        self.autoUpdate = nuke.Boolean_Knob('', 'Enable UI update', True)
        self.addKnob(self.autoUpdate)



    def knobChanged(self, knob):
        
        if self.exprCheck.value() == True:
            self.expr.setVisible(True)

            if self.expr.value() != '':
        
                for self.node in self.nodes:
        
                    try:
                        if self.expr.value() != '':
                            self.node[self.knobName].setExpression(self.expr.value())
                        else:
                            self.node[self.knobName].clearAnimated()
                            self.node[self.knobName].setValue(self.knob.value())
                    except:
                        pass

        else:
            self.expr.setVisible(False)
            for self.node in self.nodes:
                self.node[self.knobName].clearAnimated()
                

        if self.knob and self.autoUpdate.value() == True:
            for self.node in self.nodes:
                try:
                    self.node[self.knobName].setValue(self.knob.value())
                except:
                    pass
            

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
            result = KnobsChanger(knobClass,knobName,knobObject,nodes).showModalDialog()

        else:
            nuke.message("Knob does not exist")
            return

  