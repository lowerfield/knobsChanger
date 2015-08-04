
par = [] # this will remember the last entry, keep it out of the funcion

class KnobsChanger(nukescripts.PythonPanel):

    def __init__(self, knobClass, knobName, knobObject, nodes):
        nukescripts.PythonPanel.__init__( self, "Parameter Changer")

        self.knobObject = knobObject
        self.nodes = nodes
        self.knobName = knobName

        knobToChange = getattr(nuke,knobClass)

        # exceptions for those knob classes as they need more args
        if knobClass in ('Enumeration_Knob', 'Pulldown_Knob'):
            enumValues = self.knobObject.values()
            self.knob = knobToChange(knobName, knobName, enumValues)
        else:
            self.knob = knobToChange(knobName)

        # add main knob and set default value 
        self.addKnob(self.knob)
        self.knob.setValue(knobObject.value())

        # add auto update knob
        self.autoUpdate = nuke.Boolean_Knob('', 'Enable UI update')
        self.addKnob(self.autoUpdate)

        # add set expression and expression knobs 
        self.exprCheck = nuke.Boolean_Knob('Set expression')
        self.exprCheck.clearFlag(nuke.STARTLINE)
        self.addKnob(self.exprCheck)

        if knobClass in ('Enumeration_Knob', 'Pulldown_Knob'):
            self.exprCheck.setVisible(False)


        self.expr = {}      
        for pos in range(knobObject.arraySize()):
            if hasattr(knobObject, 'names'):
                name = knobObject.names(pos)
            elif knobClass == 'IArray_Knob':
                name = knobName + str(pos)
            else:
                name = knobObject.name()
            self.expr[name] = nuke.EvalString_Knob(name, '=')

        for k,v in self.expr.items():
            k = v
            k.setVisible(False)
            self.addKnob(k)

        # CALLBACKS
    def knobChanged(self, knob):
        
        # main knob callbacks    
        if self.knob and self.autoUpdate.value() == True:
            for self.node in self.nodes:
                try:                  
                    self.node[self.knobName].setValue(self.knob.value())
                    if self.node[self.knobName].hasExpression() and self.node[self.knobName].getKeyList() == []:
                        self.node[self.knobName].clearAnimation()
                        self.node[self.knobName].setValue(self.knob.value())
                    elif self.node[self.knobName].getKeyList() != []:
                        self.node[self.knobName].setExpression('')
                except:
                    pass

        # expression callbacks
        self.exprValues = []
        if self.exprCheck.value() == True:
            
            for k,v in self.expr.items():
                k = v
                k.setVisible(True)
                self.exprValues.append(k.value())

        elif self.exprCheck.value() == False:   

            for k,v in self.expr.items():
                k = v
                k.setVisible(False)

        if self.expr.items() and self.autoUpdate.value() == True:

                for k in self.exprValues:
                    for self.node in self.nodes:                                  
                        try:
                            if k != '':
                                self.node[self.knobName].setExpression(k,self.exprValues.index(k))
                            else:
                                self.node[self.knobName].setExpression('',self.exprValues.index(k))
                                self.node[self.knobName].setValue(self.knob.value())
                        except:
                                pass

        # auto update callback, if false will return[1] false so we can
        # change all the knobs outside the class
        if self.autoUpdate.value() == False:   
            self.autoUpdateF = False
        else:
            self.autoUpdateF = True

    def showModalDialog(self):
        nukescripts.PythonPanel.showModalDialog(self)

        return self.knob.value(), self.autoUpdateF, self.exprCheck.value(), self.exprValues

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

        # this updates all nodes values when autoUpdate is off
        if result[1] == False:
            for node in nodes:
                try:
                    node[knobName].setValue(result[0])
                except:
                    pass
        # this deals with the expression, only works when exprCheck is True
        if result[2] == True:

                for k in result[3]:
                    for node in nodes:                                  
                        try:
                            if k != '':
                                node[knobName].setExpression(k,result[3].index(k))
                            else:
                                node[knobName].setExpression('',result[3].index(k))
                                node[knobName].setValue(result[0])
                        except:
                                pass

