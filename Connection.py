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

MC_PRESENCE = False
CL_PRESENCE = False
EA_PRESENCE = False
''' 01. Include here the instructions for the Workbench you want to connect'''
#WN_PRESENCE = False 

def verification():

    global MC_PRESENCE
    global CL_PRESENCE
    global EA_PRESENCE
    #global WN_presence

    if 'MovieCamera' in FreeCAD.ActiveDocument.Content:
        MC_PRESENCE = True
    else:
        MC_PRESENCE = False

    if 'Clapperboard' in FreeCAD.ActiveDocument.Content:
        CL_PRESENCE = True
    else:
        CL_PRESENCE = False

    if 'ExplodedAssembly' in FreeCAD.ActiveDocument.Content:
        EA_PRESENCE = True
    else:
        EA_PRESENCE = False

    '''
    if 'WorbenchName' in FreeCAD.ActiveDocument.Content:
        WN_PRESENCE = True
    else:
        WN_PRESENCE = False
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

    from MovieCamera import MC

    '''ExplodedAssembly Workbench'''
    if MC.Cam_7Connection == 'ExplodedAssembly':
        if EA_PRESENCE == True :
            Gui.runCommand('GoToStart',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly workbench first.') + '\n')
            return

    '''03. Include here the instructions for the Workbench you want to connect'''
    '''WorkbenchName Workbench'''
    if MC.Cam_7Connection == 'WorkbenchName':
        if WN_PRESENCE == True:
            Gui.runCommand('GoToStart WorkbenchName',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first.') + '\n')
            return

# ======================================================================================
'''Play the animation'''
def connectionPlay():

    from MovieCamera import MC
    mc.modifyAnimationIndicator(Animation = True)

    '''ExplodedAssembly Workbench'''
    '''Note: In this case, the number of camera steps can be less than 
    or equal to the ExplodedAssembly. If it is smaller, the animation 
    of the objects will stop together with the camera.'''

    if MC.Cam_7Connection == 'ExplodedAssembly':

        if EA_PRESENCE == True:
            if CL_PRESENCE == True:
                CL = FreeCAD.ActiveDocument.Clapperboard
                if CL.Cam_3OnRec == True:
                    rpv.runRecordCamera()
            Gui.runCommand('PlayForward',0)
            mc.modifyAnimationIndicator(Animation = False)
            if CL_PRESENCE == True:
                CL = FreeCAD.ActiveDocument.Clapperboard
                CL.Cam_3OnRec = False

        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly workbench first.') + '\n')
            return

    '''04. Include here the instructions for the Workbench you want to connect'''
    '''WorkbenchName Workbench'''

    if MC.Cam_7Connection == 'WorkbenchName':

        if WN_PRESENCE == True:
            import WorkbenchName as wn
            steps = MC.Anim_3EndStep - MC.Anim_4CurrentStep

            if MC.Cam_Target == 'Follow the route':
                steps = steps - MC.Cam_Target_Steps_Forward

            if CL_PRESENCE == True:
                CL = FreeCAD.ActiveDocument.Clapperboard

            for p in range (steps):
                Gui.updateGui()

                '''Clapperboard records a frame'''
                if CL_PRESENCE == True:
                    if CL.Cam_3OnRec == True:
                        rpv.runRecordCamera()

                '''Movie Camera takes a step forward'''
                mc.postMovieCamera(condition = 'next')

                '''WorkbenchName takes a step forward'''
                try:
                    wn.runStepbyStepAnimation() # Animating step by step before Gui.updateGui()
                except:
                    wn.stepStep = True # Instruction for animating pause step by step before Gui.updateGui()
                    wn.runAnimation()

                '''Pause the connectionPlay'''
                if MC.Cam_8OnAnim == False:
                   wn.pauseAnimation # Pause animation WorkbenchName command/instruction
                   break

            wn.stopAnimation # Stop animation WorkbenchName command/instruction (if not so)
            mc.modifyAnimationIndicator(Animation = False)
            if CL_PRESENCE == True:
                CL = FreeCAD.ActiveDocument.Clapperboard
                CL.Cam_3OnRec = False
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first.') + '\n')
            return
    '''Enable the next camera, if so'''
    mc.nextMovieCamera(condition = 'play')
# ====================================================================================== 
'''Pause the animation'''
def connectionPause():

    from MovieCamera import MC

    '''ExplodedAssembly Workbench'''
    if MC.Cam_7Connection == 'ExplodedAssembly':
        if EA_PRESENCE == True :
            Gui.runCommand('StopAnimation',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly Workbench first.') + '\n')
            return

    '''05. Include here the instructions for the Workbench you want to connect'''
    '''WorkbenchName Workbench'''
    if MC.Cam_7Connection == 'WorkbenchName':
        if WN_PRESENCE == True:
            Gui.runCommand('PauseAnimationWorkbenchName',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first.') + '\n')
            return
# ====================================================================================== 
'''Go to the end of the animation'''
def connectionEnd():

    from MovieCamera import MC
    '''ExplodedAssembly Workbench'''
    if MC.Cam_7Connection == 'ExplodedAssembly':
        if EA_PRESENCE == True :
            Gui.runCommand('GoToEnd',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly workbench first.') + '\n')
            return

    '''06. Include here the instructions for the Workbench you want to connect'''
    '''WorkbenchName Workbench'''
    if MC.Cam_7Connection == 'WorkbenchName':
        if WN_PRESENCE == True:
            Gui.runCommand('GoToEndWorkbenchName',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first.') + '\n')
            return

# ====================================================================================== 

'''Only from ExplodedAssembly Workbench'''

def connectionEA():

    EA = FreeCAD.ActiveDocument.ExplodedAssembly
    from MovieCamera import MC
    # 1. From play MC:
    if MC_PRESENCE == True and MC.Cam_7Connection == 'ExplodedAssembly' and MC.Cam_8OnAnim == True:
        mc.postMovieCamera(condition = 'next')
        if MC.Cam_8OnAnim == False:
            EA.InAnimation = False
    if CL_PRESENCE == True:
        CL = FreeCAD.ActiveDocument.Clapperboard
        if CL.Cam_3OnRec == True:
            rpv.runRecordCamera()
            if EA.InAnimation == False:
                rpv.stopRecordCamera()

    else:
        pass

# ======================================================================================
