import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')

import clr
clr.AddReferenceByName("Eto")
clr.AddReferenceByName("Rhino.UI")

import Rhino
import scriptcontext
import System
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
import subprocess

from USimulation.modelPrep import rhinoOutput
from UTool.dirLocation import DirUsr

import subprocess

 
class EtoDialog(forms.Dialog[bool]):
 
    # Dialog box Class initializer
    def __init__(self):
        # Initialize dialog box
        self.Title = 'LUMENVR: Shaping daylight in Virtual Reality'
        self.Padding = drawing.Padding(100)
        self.Resizable = False
        self.ClientSize = drawing.Size(800, 800)
 
        
        # Create controls for the dialog
        'header'
        self.workflowH = forms.Label(Text = 'lumenVR workflow',
                                     VerticalAlignment = forms.VerticalAlignment.Center, 
                                     TextAlignment = forms.TextAlignment.Left
                                    )
        
        self.L_weather = forms.Label(Text = 'import weather file:')
        self.B_weather = forms.Button(Text = 'weather file')
        
        self.L_north = forms.Label(Text = 'North offset:')
        self.T_north = forms.TextBox(Text = None)
 
        self.L_MCeil = forms.Label(Text = 'materials for CEILING:')
        self.T_MCeil = forms.TextBox(Text = None)   
        
        self.L_MCol = forms.Label(Text = 'materials for COLUMN:')
        self.T_MCol = forms.TextBox(Text = None)   
        
        self.L_MFl = forms.Label(Text = 'materials for FLOOR:')
        self.T_MFl = forms.TextBox(Text = None)   
        
        self.L_MGlaz = forms.Label(Text = 'materials for GLAZING:')
        self.T_MGlaz = forms.TextBox(Text = None)   
        
        self.L_MMul = forms.Label(Text = 'materials for MULLION:')
        self.T_MMul = forms.TextBox(Text = None)    
        
        self.L_MPar = forms.Label(Text = 'materials for PARTITION:')
        self.T_MPar = forms.TextBox(Text = None)    
        
        self.L_MSHAD = forms.Label(Text = 'materials for SHADE:')
        self.T_MSHAD = forms.TextBox(Text = None)    
        
        self.L_Sensor = forms.Label(Text = 'Set up sensor points:')
        self.T_Sensor = forms.TextBox(Text = None)   
        
        # Create the default button
        self.radButton = forms.Button(Text = 'export to Radiance Model')
        self.radButton.Click += self.OnOKButtonClick
        
        # Create the default button
        self.UEButton = forms.Button(Text = 'open UEditor')
        self.UEButton.Click += self.OnUEButtonClick
 
        # Create the abort button
        self.AbortButton = forms.Button(Text = 'Cancel')
        self.AbortButton.Click += self.OnCloseButtonClick
 
        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(10, 10)
        
        layout.AddRow(self.workflowH)
        layout.AddRow(None) # spacer
        layout.AddRow(None) # spacer
        layout.AddRow(None) # spacer
        layout.AddRow(None) # spacer
        layout.AddRow(None) # spacer
        
        layout.AddRow(self.L_weather, self.B_weather)
        layout.AddRow(None) # spacer
        
        layout.AddRow(self.L_north, self.T_north)
        layout.AddRow(None) # spacer
        
        layout.AddRow(self.L_MCeil, self.T_MCeil)

        
        layout.AddRow(self.L_MCol, self.T_MCol)

        
        layout.AddRow(self.L_MFl, self.T_MFl)

        
        layout.AddRow(self.L_MGlaz, self.T_MGlaz)
     
        
        layout.AddRow(self.L_MMul, self.T_MMul)
   
        
        layout.AddRow(self.L_MPar, self.T_MPar)
  
        
        layout.AddRow(self.L_MSHAD, self.T_MSHAD)
        layout.AddRow(self.L_Sensor, self.T_Sensor)
        layout.AddRow(None) # spacer
        layout.AddRow(None) # spacer
        layout.AddRow(None) # spacer
        layout.AddRow(None) # spacer
        layout.AddRow(None) # spacer
        
        layout.AddRow(self.radButton, self.UEButton)

        
        # Set the dialog content
        self.Content = layout
 
    # Start of the class functions
 
    # Get the value of the textbox
    def GetText(self):
        return self.T_MMul

    # Close button click handler
    def OnCloseButtonClick(self, sender, e):
        self.T_MMul = ""
        self.Close(False)
 
    # OK button click handler
    def OnOKButtonClick(self, sender, e):
        rhinoOutput.rhinoModelPrep()
        self.Close(False)
            
    # OK button click handler
    def OnUEButtonClick(self, sender, e):
        Editor = "C:\\Program Files\\Epic Games\\UE_5.1\\Engine\\Binaries\\Win64\\UnrealEditor.exe"
        projectPath = "E:\\CMU\\thesis\\1125\\initialLumen11\\initial.uproject"

        cmd = (Editor + ' ' + projectPath)
        subprocess.call(cmd)
        self.Close(True)

################################################################################
# The script that will be using the dialog.
def openGUI():
    dialog = EtoDialog()
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.GetText() #Print the Number from the dialog control
    
 
