
par = [] # this will remember the last entry, keep it out of the funcion

class KnobsChanger(nukescripts.PythonPanel):

    def __init__(self, knobClass, knobName, knobObject, nodes):
        nukescripts.PythonPanel.__init__( self, "Parameter Changer")

        self.knobClass = knobClass 
        self.knobObject = knobObject
        self.nodes = nodes
        self.knobName = knobName

        knobToChange = getattr(nuke,knobClass)

        # set source knobs dictionary
        self.knob = {}

        if knobClass in ('Enumeration_Knob', 'Pulldown_Knob'):
            enumValues = self.knobObject.values()
            self.knob[self.knobName] = knobToChange(knobName, knobName, enumValues)

        elif knobClass == 'IArray_Knob':

            for pos in range(knobObject.arraySize()):
                name = str(pos)
                self.knob[name] = knobToChange(knobName, name)
        else:
            self.knob[self.knobName] = knobToChange(knobName)

        # add source knobs
        if knobClass == 'IArray_Knob':
            count = 0
            for k,v in sorted(self.knob.items()):
                k = v
                self.addKnob(k)
                if count % self.knobObject.width() != 0:
                    k.clearFlag(nuke.STARTLINE)
                count += 1
        else:
            for k,v in self.knob.items():
                k = v
                self.addKnob(k)
                k.setValue(knobObject.value())

        # add auto update knob
        self.autoUpdate = nuke.Boolean_Knob('', 'Enable UI update')
        self.addKnob(self.autoUpdate)

        # add set expression and expression knobs 
        self.exprCheck = nuke.Boolean_Knob('Set expression')
        self.exprCheck.clearFlag(nuke.STARTLINE)
        self.addKnob(self.exprCheck)

        if knobClass in ('Enumeration_Knob', 'Pulldown_Knob'):
            self.exprCheck.setVisible(False)

        # set expressions knobs dictionary
        self.expr = {}

        if hasattr(knobObject,'arraySize'):       
            for pos in range(knobObject.arraySize()):
                name = knobObject.name() + str(pos)
                self.expr[name] = nuke.EvalString_Knob(name, '=')
        else:
            name = knobObject.name()
            self.expr[name] = nuke.EvalString_Knob(name, '=')

        # add expression knobs
        for k,v in self.expr.items():
            k = v
            self.addKnob(k)
            k.setVisible(False)

        # CALLBACKS
    def knobChanged(self, knob):
     
        # source knob callbacks 
        self.knobValues = {}
        for k in sorted(self.knob.keys()): 
            if self.knob[k] and self.autoUpdate.value() == True:
                for self.node in self.nodes:
                    try:
                        if self.knobClass == 'IArray_Knob':
                            self.knobSetValue = self.node[self.knobName].setValue(self.knob[k].value(),int(k))
                        else:
                            self.knobSetValue = self.node[self.knobName].setValue(self.knob[self.knobName].value())
                        if self.node[self.knobName].hasExpression() and self.node[self.knobName].getKeyList() == []:
                            self.node[self.knobName].clearAnimation()
                            self.knobSetValue
                        elif self.node[self.knobName].getKeyList() != []:
                            self.node[self.knobName].setExpression('',int(k))
                    except:
                        pass

            elif self.knob[k] and self.autoUpdate.value() == False:
                self.knobValues[k] = self.knob[k].value()

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
                                if self.knobClass == 'IArray_Knob':
                                    self.node[self.knobName].setValue(self.knob[k].value(),int(k))
                                else:
                                    self.node[self.knobName].setValue(self.knob[self.knobName].value())
                        except:
                                pass

        # auto update callback, if false will return[1] false so we can
        # change all the knobs outside the class, when the panle is closed
        if self.autoUpdate.value() == False:   
            self.autoUpdateF = False
        else:
            self.autoUpdateF = True

        if self.knobClass == 'IArray_Knob':
            self.knobValues = self.knobValues
        else:
            self.knobValues = self.knob[self.knobName].value()

    def showModalDialog(self):
        nukescripts.PythonPanel.showModalDialog(self)

        return self.knobValues, self.autoUpdateF, self.exprCheck.value(), self.exprValues, self.knob

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
                if knobClass == 'IArray_Knob':
                    for k,v in sorted(result[0].items()):
                        node[knobName].setValue(int(v),int(k))
                else:
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
