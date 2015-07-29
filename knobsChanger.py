
class Test( nukescripts.PythonPanel ):
    def __init__( self):
        nukescripts.PythonPanel.__init__( self, "test")

        node = nuke.selectedNode()    
        param = nuke.getInput('Parameter to change', '')
        n =  node[param].Class()
        knobT = getattr(nuke,n)
        self.knob = knobT(param)
        self.addKnob(self.knob)

    def showModalDialog(self):
        nukescripts.PythonPanel.showModalDialog(self)

	return self.knob.value()

Test().showModalDialog()