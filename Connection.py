''' Movie Workbench, Connection Module '''

# ***************************************************************************
# *   Copyright (c) 2023 Francisco Rosa                                     *   
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/

import FreeCADGui as Gui
import FreeCAD
from PySide.QtCore import QT_TRANSLATE_NOOP
import os
import MovieCamera as mc
import RecordPlayVideo as rpv

translate = FreeCAD.Qt.translate

LanguagePath = os.path.dirname(__file__) + '/translations'
Gui.addLanguagePath(LanguagePath)

'''INSTRUCTIONS'''
'''
This is the module for connecting the Movie Workbench with other object animation 
workbenches. You can add them, according to the indicated numbered (01 to 06) suggestions, 
always coping, carrying out all necessary adaptations and tests then before finalizing the 
additions. The connection works only with the first Movie Camera created.
'''
# ====================================================================================== 
# 0. Global

MC_presence = False
CL_presence = False
EA_presence = False
''' 01. Include here the instructions for the Workbench you want to connect'''
#WN_presence = False 

def verification():

    global MC_presence
    global CL_presence
    global EA_presence
    #global WN_presence
        
    if 'MovieCamera' in FreeCAD.ActiveDocument.Content:       
        MC_presence = True
    else:
        MC_presence = False
        
    if 'Clapperboard' in FreeCAD.ActiveDocument.Content:        
        CL_presence = True
    else:
        CL_presence = False 

    if 'ExplodedAssembly' in FreeCAD.ActiveDocument.Content:        
        EA_presence = True      
    else:
        EA_presence = False
        
    '''   
    if 'WorbenchName' in FreeCAD.ActiveDocument.Content:        
        WN_presence = True      
    else:
        WN_presence = False
    '''
# ======================================================================================  
# 1. Connection list

'''02.Include in the connection list the name of the Workbench you want to connect'''

connections = ['None', 'ExplodedAssembly']

# ====================================================================================== 
# 2. Functions

# ====================================================================================== 
'''Go to the beginning of the animation'''
def connectionIni():
	
    MC = FreeCAD.ActiveDocument.MovieCamera
    
    '''ExplodedAssembly Workbench'''
    if MC.Cam_3Connection == 'ExplodedAssembly':       
        if EA_presence == True :
            Gui.runCommand('GoToStart',0)                                                                                                      
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly workbench first.') + '\n')
            return

    '''03. Include here the instructions for the Workbench you want to connect'''
    '''WorkbenchName Workbench'''
    if MC.Cam_3Connection == 'WorkbenchName':
        if WN_presence == True:
            Gui.runCommand('GoToStart WorkbenchName',0)                                                                                                   
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first.') + '\n')
            return

# ====================================================================================== 
'''Play the animation'''
def connectionPlay():
	
    MC = FreeCAD.ActiveDocument.MovieCamera

    '''ExplodedAssembly Workbench'''    
    '''Note: In this case, the number of camera steps can be less than 
    or equal to the ExplodedAssembly. If it is smaller, the animation 
    of the objects will continue without the animation of the camera, 
    but if it is greater, the camera will not continue to animate 
    without the movement of the objects.'''
    
    if MC.Cam_3Connection == 'ExplodedAssembly':

        if EA_presence == True:
            if CL_presence == True:
                CL = FreeCAD.ActiveDocument.Clapperboard
                if CL.Cam_3OnRec == True:
                    rpv.runRecordCamera()            
            Gui.runCommand('PlayForward',0)
            MC.Cam_4OnAnim = False
            if CL_presence == True:
                CL = FreeCAD.ActiveDocument.Clapperboard
                CL.Cam_3OnRec = False
                
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly workbench first.') + '\n')
            return

    '''04. Include here the instructions for the Workbench you want to connect'''
    '''WorkbenchName Workbench'''

    if MC.Cam_3Connection == 'WorkbenchName':
    	
        if WN_presence == True:
            import WorkbenchName as wn  
            steps = MC.Anim_3EndStep - MC.Anim_4CurrentStep

            if MC.Cam_Target == 'Follow the route':
                steps = steps - MC.Cam_Target_Steps_Forward           

            if CL_presence == True:               
                CL = FreeCAD.ActiveDocument.Clapperboard

            for p in range (steps):
                Gui.updateGui()
                
                '''Clapperboard records a frame'''
                if CL_presence == True:
                    if CL.Cam_3OnRec == True:
                        rpv.runRecordCamera()
                
                '''Movie Camera takes a step forward'''
                mc.postMovieAnimation()
            
                '''WorkbenchName takes a step forward'''                        
                try:
                    wn.runStepbyStepAnimation() # Animating step by step before Gui.updateGui()
                except:            
                    wn.stepStep = True # Instruction for animating pause step by step before Gui.updateGui()
                    wn.runAnimation()
                
                '''Pause the connectionPlay'''       
                if MC.Cam_4OnAnim == False:
                   wn.pauseAnimation # Pause animation WorkbenchName command/instruction
                   break
                   
            wn.stopAnimation # Stop animation WorkbenchName command/instruction (if not so)  
                    
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first.') + '\n')
            return
# ====================================================================================== 
'''Pause the animation'''           
def connectionPause():
	
    MC = FreeCAD.ActiveDocument.MovieCamera
    
    '''ExplodedAssembly Workbench'''
    if MC.Cam_3Connection == 'ExplodedAssembly':
        if EA_presence == True :
            Gui.runCommand('StopAnimation',0)                                                                                                   
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly Workbench first.') + '\n')
            return

    '''05. Include here the instructions for the Workbench you want to connect'''
    '''WorkbenchName Workbench'''
    if MC.Cam_3Connection == 'WorkbenchName':
        if WN_presence == True:
            Gui.runCommand('PauseAnimationWorkbenchName',0)                                                                                                  
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first.') + '\n')
            return
# ====================================================================================== 
'''Go to the end of the animation'''
def connectionEnd():
	
    MC = FreeCAD.ActiveDocument.MovieCamera
    
    '''ExplodedAssembly Workbench'''
    if MC.Cam_3Connection == 'ExplodedAssembly':
        if EA_presence == True :
            Gui.runCommand('GoToEnd',0)                                                 
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly workbench first.') + '\n')
            return          

    '''06. Include here the instructions for the Workbench you want to connect'''
    '''WorkbenchName Workbench'''
    if MC.Cam_3Connection == 'WorkbenchName':
        if WN_presence == True:
            Gui.runCommand('GoToEndWorkbenchName',0)                                                                                                    
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first.') + '\n')
            return

# ====================================================================================== 

'''Only from ExplodedAssembly Workbench'''  

def connectionEA():

    EA = FreeCAD.ActiveDocument.ExplodedAssembly
    MC = FreeCAD.ActiveDocument.MovieCamera
    # 1. From play MC:     
    if MC.Cam_3Connection == 'ExplodedAssembly' and MC.Cam_4OnAnim == True:
        import MovieCamera as mc
        mc.postMovieAnimation()
        if MC.Cam_4OnAnim == False:
            EA.InAnimation = False                   
    if CL_presence == True:
        CL = FreeCAD.ActiveDocument.Clapperboard
        if CL.Cam_3OnRec == True:
            rpv.runRecordCamera()
            if EA.InAnimation == False:
                rpv.stopRecordCamera()
                        
    else:
        pass                                  

# ======================================================================================              