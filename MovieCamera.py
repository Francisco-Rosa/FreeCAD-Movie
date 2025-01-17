''' Movie Workbench, Movie Camera animation toolbar '''

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

import FreeCAD
import FreeCADGui as Gui
from pivy import coin
import os
import time
from math import degrees, radians
from PySide.QtCore import QT_TRANSLATE_NOOP
import MovieConnection as co
import MovieAnimation as ma

translate = FreeCAD.Qt.translate

LanguagePath = os.path.dirname(__file__) + '/translations'
Gui.addLanguagePath(LanguagePath)

# ======================================================================================
# 0. Global

MC = None

def enableCameraSelection(Enable = None):
    global MC
    MC = Enable

# ======================================================================================
# 1. Classes

class MovieCamera:
    '''Class to create a camera to be animated'''

    def __init__(self, obj):

    # Movie Camera 1 - Animation config

        obj.addProperty('App::PropertyInteger', 'Cam_01AnimIniStep', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Initial step of the MovieCamera animation. Indicate the step which this section of '
                                                    'the animation will begin.')).Cam_01AnimIniStep = 0
        obj.addProperty('App::PropertyInteger', 'Cam_02AnimCurrentStep', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Current step of the MovieCamera animation. It is only indicative.')).Cam_02AnimCurrentStep = 0
        obj.addProperty('App::PropertyInteger', 'Cam_03AnimEndStep', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'End step of the MovieCamera animation. Indicate the step which this section of the animation '
                                                    'will finish. Changes will only take effect after MovieCamera has been re-enabled.'
                                                    )).Cam_03AnimEndStep = 100
        obj.addProperty('App::PropertyInteger', 'Cam_04AnimTotalSteps', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Total steps of the MovieCamera animation. It is the result of the difference between end step '
                                                    '(“Cam_03AnimEndStep”) and initial step (“Cam_01AnimIniStep”).'
                                                    )).Cam_04AnimTotalSteps = 100
        obj.addProperty('App::PropertyInteger', 'Cam_05AnimFps', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Animation fps of the MovieCamera. Specify the value for this animation section. '
                                                    'It is a simulation and will depend on the '
                                                    'computer performance. Changes will only take '
                                                    'effect after MovieCamera has been re-enabled.')).Cam_05AnimFps = 30
        obj.addProperty('App::PropertyString', 'Cam_06AnimTime', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Animation time of the MovieCamera, in hours, minutes, and seconds. '
                                                    'It is only indicative.'
                                                    )).Cam_06AnimTime = time.strftime('%H:%M:%S', time.gmtime(3.33))
        obj.addProperty('App::PropertyBool', 'Cam_07OnAnim', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'MovieCamera animation on or off. '
                                                    'It should not be changed manually, it is controlled by the animation buttons.'
                                                    )).Cam_07OnAnim = False

    # Movie Camera 02 - Camera config

        obj.addProperty('App::PropertyEnumeration', 'Cam_01Type', 'Movie Camera 02 - Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Camera type for the MovieCamera. Choose the camera through which this section of '
                                                    'the animation will be performed: “3DView” for 3D views and the “Render” for '
                                                    'adopting the settings of a camera from the Render Workbench, previously created and adjusted.'
                                                    )).Cam_01Type = ('3DView', 'Render')
        obj.addProperty('App::PropertyLink', 'Cam_02Render_Selection', 'Movie Camera 02 - Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Render camera selection for the MovieCamera animation. If you have chosen “Render” '
                                                    'in Camera type (“Cam_01Type”), you have to select which one will be used in this '
                                                    'section of the animation.'
                                                    )).Cam_02Render_Selection = None
        obj.addProperty('App::PropertyInteger', 'Cam_03RenderWidth', 'Movie Camera 02 - Camera config',  QT_TRANSLATE_NOOP('App::Property',
                                                    'Render image width of the MovieCamera animation. Configure the width in pixels that will '
                                                    'compose the aspect ratio of the image (“AspectRatio”).'
                                                    )).Cam_03RenderWidth = 800
        obj.addProperty('App::PropertyInteger', 'Cam_04RenderHeight', 'Movie Camera 02 - Camera config',  QT_TRANSLATE_NOOP('App::Property',
                                                    'Render image height of the MovieCamera animation. Configure the height in pixels that will '
                                                    'compose the aspect ratio of the image (“AspectRatio”).'
                                                    )).Cam_04RenderHeight = 600
        obj.addProperty('App::PropertyLinkList', 'Cam_05ObjectsSelected', 'Movie Camera 02 - Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Objects selected for the MovieCamera animation. Select the MoveObjects to animate '
                                                    'together with this MovieCamera.')).Cam_05ObjectsSelected = None
        obj.addProperty('App::PropertyEnumeration', 'Cam_06Enable', 'Movie Camera 02 - Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Enable the combinations for the MovieCamera animation. Configure the combination of '
                                                    'objects to animate together: only MovieCamera (“Camera”), MovieCamera and MovieObjects '
                                                    '(“Camera and objects”), MovieCamera and connection (“Camera and connection”), '
                                                    'or even just the MovieObjects (“Objects”) or connection (“Connection”) associated with '
                                                    'this MovieCamera. For each combination change it will be necessary to re-enable the '
                                                    'MovieCamera (Enable a MovieCamera button).'
                                                    )).Cam_06Enable = ('Camera', 'Camera and objects', 'Objects', 'Camera and connection', 'Connection')
        obj.addProperty('App::PropertyEnumeration', 'Cam_07Connection', 'Movie Camera 02 - Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Connection for MovieCamera animation. '
                                                    'Choose the workbench through which the animation will be performed together, if so. '
                                                    'Make sure the workbench is installed and that there '
                                                    'is an animation created with it.'
                                                    )).Cam_07Connection = list(co.connections)

    # Movie Camera 03 - Target config

        obj.addProperty('App::PropertyEnumeration', 'Cam_01Target', 'Movie Camera 03 - Target config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Target of the MovieCamera. '
                                                    'If you want to use an object or point as a target, choose Follow an object or point '
                                                    '(“Follow an object or point”) and select one of them in Target object selection '
                                                    '(“Cam_02Target_ObjectSelection”), while for the Follow a route (“Follow a route”) '
                                                    'option you must use Route selection (“Cam_02RouteSelection”).'
                                                    )).Cam_01Target = ('Free', 'Follow an object or point', 'Follow a route')
        obj.addProperty('App::PropertyLink', 'Cam_02TargetObjectSelection', 'Movie Camera 03 - Target config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Target object selection of the MovieCamera. Select the point or object you want the camera to point to.'
                                                    )).Cam_02TargetObjectSelection = None
        obj.addProperty('App::PropertyInteger', 'Cam_03TargetStepsForward', 'Movie Camera 03 - Target config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Target ahead of the MovieCamera. If you chose for the target to “follow a route”, '
                                                    'in “Cam_01Target”, you need to specify how many steps this target will be ahead of the camera '
                                                    'on the same route.'
                                                    )).Cam_03TargetStepsForward = 10

    # Movie Camera 04 - Camera follows a path

        obj.addProperty('App::PropertyBool', 'Cam_01Route', 'Movie Camera 04 - Camera follows a path', 
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Route of the MovieCamera animation. Choose “true” if the camera will be animate on a route. '
                                                    'You have to select a single segment on Route selection (“Cam_02RouteSelection”) to use it.'
                                                    )).Cam_01Route = False
        obj.addProperty('App::PropertyLink', 'Cam_02RouteSelection', 'Movie Camera 04 - Camera follows a path', 
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Route selection for the MovieCamera animation. Choose the route through which the camera will be '
                                                    'animate. You have to select a single segment such as: line, arc, circle, '
                                                    'ellipse, B-spline or Bézier curve, from Sketcher or Draft Workbenches.'
                                                    )).Cam_02RouteSelection = None

    # Movie Camera 05 - Camera Pos A-B - pos On/Off

        obj.addProperty('App::PropertyBool', 'Cam_01XMov', 'Movie Camera 05 - Camera Pos A-B - pos On/Off', QT_TRANSLATE_NOOP('App::Property', 
                                                    'X movement of the MovieCamera. Choose “true”, if you want to animate the camera in X direction.'
                                                    )).Cam_01XMov = False
        obj.addProperty('App::PropertyBool', 'Cam_02YMov', 'Movie Camera 05 - Camera Pos A-B - pos On/Off', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Y movement of the MovieCamera. Choose “true”, if you want to animate the camera in Y direction.'
                                                    )).Cam_02YMov = False
        obj.addProperty('App::PropertyBool', 'Cam_03ZMov', 'Movie Camera 05 - Camera Pos A-B - pos On/Off', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Z movement of the MovieCamera. Choose “true”, if you want to animate the camera in Z direction.'
                                                    )).Cam_03ZMov = False

    # Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off

        obj.addProperty('App::PropertyBool', 'Cam_01Yaw', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Yaw of the MovieCamera. Choose “true”, if you want '
                                                    'to animate the camera horizontal angle.')).Cam_01Yaw = False
        obj.addProperty('App::PropertyBool', 'Cam_02Pitch', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Pitch of the MovieCamera. Choose “true”, if you want '
                                                    'to animate the camera vertical angle.')).Cam_02Pitch = False
        obj.addProperty('App::PropertyBool', 'Cam_03Roll', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Roll of the MovieCamera. Choose “true”, if you want '
                                                    'to animate the camera roll angle.')).Cam_03Roll = False
        obj.addProperty('App::PropertyBool', 'Cam_04Zoom', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Zoom of the MovieCamera. Choose “true”, if you want to animate the camera zoom.'
                                                    )).Cam_04Zoom = False

    # Movie Camera 07 - Camera Pos A-B - pos AB 

        obj.addProperty('App::PropertyFloat', 'Cam_01XPosA', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                    'X of Position A of the MovieCamera. It is set when the Set position A button is pressed, after that, '
                                                    'if necessary, you can make adjustments to the x-value.')).Cam_01XPosA = 0
        obj.addProperty('App::PropertyFloat', 'Cam_02YPosA', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Y of Position A of the MovieCamera. It is set when the Set position A button is pressed, after that, '
                                                    'if necessary, you can make adjustments to the y-value.')).Cam_02YPosA = 0
        obj.addProperty('App::PropertyFloat', 'Cam_03ZPosA', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                     'Z of Position A of the MovieCamera. It is set when the Set position A button is pressed, after that, '
                                                     'if necessary, you can make adjustments to the z-value.')).Cam_03ZPosA = 0
        obj.addProperty('App::PropertyFloat', 'Cam_04XPosB', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                    'X of Position B of the MovieCamera. It is set when the Set position B button is pressed, after that, '
                                                    'if necessary, you can make adjustments to the x-value.')).Cam_04XPosB = 1000.0
        obj.addProperty('App::PropertyFloat', 'Cam_05YPosB', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Y of Position B of the MovieCamera. It is set when the Set position B button is pressed, after that, '
                                                    'if necessary, you can make adjustments to the y-value.')).Cam_05YPosB = 1000.0
        obj.addProperty('App::PropertyFloat', 'Cam_06ZPosB', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Z of Position B of the MovieCamera. It is set when the Set position B button is pressed, after that, '
                                                    'if necessary, you can make adjustments to the z-value.')).Cam_06ZPosB = 1000.0

    # Movie Camera 08 - Camera Pos A-B - angles

        obj.addProperty('App::PropertyAngle', 'Cam_01YawPosA', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Yaw of Position A of the MovieCamera. It is set when the Set position A button '
                                                    'is pressed, after that, if necessary, you can make little adjustments to the horizontal angle '
                                                    'value of the camera.')).Cam_01YawPosA = 0
        obj.addProperty('App::PropertyAngle', 'Cam_02PitchPosA', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Pitch of Position A of the MovieCamera. It is set when the Set position A button '
                                                    'is pressed, after that, if necessary, you can make little adjustments to the vertical angle '
                                                    'value of the camera.')).Cam_02PitchPosA = 0
        obj.addProperty('App::PropertyAngle', 'Cam_03RollPosA', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Roll of Position A of the MovieCamera. It is set when the Set position A button '
                                                    'is pressed, after that, if necessary, you can make little adjustments to the roll value of the camera.'
                                                    )).Cam_03RollPosA = 90
        obj.addProperty('App::PropertyAngle', 'Cam_04YawPosB', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Yaw of Position B of the MovieCamera. It is set when the Set position B button '
                                                    'is pressed, after that, if necessary, you can make little adjustments to the horizontal angle value '
                                                    'of the camera.')).Cam_04YawPosB = 30
        obj.addProperty('App::PropertyAngle', 'Cam_05PitchPosB', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Pitch of Position B of the MovieCamera. It is set when the Set position B button '
                                                    'is pressed, after that, if necessary, you can make little adjustments to the vertical angle value '
                                                    'of the camera.')).Cam_05PitchPosB = 45
        obj.addProperty('App::PropertyAngle', 'Cam_06RollPosB', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Roll of Position B of the MovieCamera. It is set when the Set position B button '
                                                    'is pressed, after that, if necessary, you can make little adjustments to the roll value of the camera.'
                                                    )).Cam_06RollPosB = 45

    # Movie Camera 09 - Camera Pos A-B - Zoom

        obj.addProperty('App::PropertyAngle', 'Cam_02ZoomPosA', 'Movie Camera 09 - Camera Pos A-B - Zoom', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Zoom of Position A of the MovieCamera. If Zoom of the MovieCamera (“Cam_04Zoom”) '
                                                    'is “true” and after the Set position A button is pressed, '
                                                    'you can adjust the angle in degrees you want to start the '
                                                    'camera animation. Decreasing the value to zoom in and increasing to zoom out.'
                                                    )).Cam_02ZoomPosA = 50
        obj.addProperty('App::PropertyAngle', 'Cam_03ZoomPosB', 'Movie Camera 09 - Camera Pos A-B - Zoom', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Zoom of Position B of the MovieCamera. If Zoom of the MovieCamera (“Cam_04Zoom”) '
                                                    'is “true” and after the Set position B button is pressed, '
                                                    'you can adjust the angle in degrees you want to finish the '
                                                    'camera animation. Decreasing the value to zoom in and increasing to zoom out.'
                                                    )).Cam_03ZoomPosB = 20

        obj.Proxy = self

class MovieCameraViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/MovieCameraIcon.svg'

# ======================================================================================    
# 2. Command classes

class CreateMovieCamera:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/CreateMovieCameraIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('CreateMovieCamera', 'MovieCamera'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateMovieCamera', 'Create a MovieCamera. '
                                              'Initially, a static camera is created. To make '
                                              'it go from position A to position B, enable it, '
                                              'follow the positions A and B instructions, and start '
                                              'the animation. For the other possibilities,  adjust '
                                              'the corresponding necessary settings (properties '
                                              'window), enable it and start the animation.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        global MC
        ActivatedMovieCamera(self)
        MC.Cam_07OnAnim = False
        # Provisional AB Positions
        setMCPosA(Option = MC)
        setMCPosB(Option = MC)
        FreeCAD.Console.PrintMessage(translate('Movie', 'A static MovieCamera was created! '
                                               'To animate the camera establish its A and B positions, or '
                                               'make the adjustments in its properties window.') + '\n')

def ActivatedMovieCamera(self):
    global MC
    default_label = translate('Movie', 'MovieCamera')
    folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'MovieCamera')
    MovieCamera(folder)
    MovieCameraViewProvider(folder.ViewObject)
    MC = folder
    MC.Label = default_label

# ======================================================================================

class EnableMovieCamera:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/EnableMovieCameraIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('EnableMovieCamera', 'Enable a MovieCamera'),
                'ToolTip': QT_TRANSLATE_NOOP('EnableMovieCamera', 
                                             'First, select a MovieCamera that you want to configure, '
                                             'then click on this button to activate it.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        ma.enableMovieSelection(Enable = 'Camera')

# ======================================================================================  
# 3. Functions

def setMCPosA(Option = None):

    MC = Option
    Gui.runCommand('Std_PerspectiveCamera',1)

    if MC.Cam_01Target == 'Free':
        MC.Cam_01XMov = True
        MC.Cam_02YMov = True
        MC.Cam_03ZMov = True
        MC.Cam_01Yaw = True
        MC.Cam_02Pitch = True
        MC.Cam_03Roll = True
        MC.Cam_04Zoom = True

    if MC.Cam_01Target == 'Follow an object or point' :
        MC.Cam_01XMov = True
        MC.Cam_02YMov = True
        MC.Cam_03ZMov = True
        MC.Cam_01Yaw = False
        MC.Cam_02Pitch = False
        MC.Cam_03Roll = False
        MC.Cam_04Zoom = True

    # Camera node position A
    cameraNodeA = Gui.ActiveDocument.ActiveView.getCameraNode()

    # Camera position A
    vectorNodeA = FreeCAD.Vector(cameraNodeA.position.getValue())
    MC.Cam_01XPosA = vectorNodeA[0]
    MC.Cam_02YPosA = vectorNodeA[1]
    MC.Cam_03ZPosA = vectorNodeA[2]

    # Camera angles pos A
    rotNodeA = FreeCAD.Rotation(*cameraNodeA.orientation.getValue().getValue())
    anglesYawPitchRollA = rotNodeA.getYawPitchRoll()
    MC.Cam_01YawPosA = anglesYawPitchRollA[0]
    MC.Cam_02PitchPosA = anglesYawPitchRollA[1]
    MC.Cam_03RollPosA = anglesYawPitchRollA[2]

    # Camera zoom pos A
    MC.Cam_02ZoomPosA = degrees(float(cameraNodeA.heightAngle.getValue()))

    # Render camera angles and zoom pos A
    if MC.Cam_01Type == 'Render':
        if 'Camera' in FreeCAD.ActiveDocument.Content and MC.Cam_02Render_Selection:
            renderCameraA = MC.Cam_02Render_Selection
            renderCameraA.ViewObject.Proxy.set_camera_from_gui()
            renderCameraA.AspectRatio = MC.Cam_03RenderWidth/MC.Cam_04RenderHeight
            renderCameraA.ViewportMapping = 'CROP_VIEWPORT_FILL_FRAME'
            renderCameraA.ViewObject.Proxy.set_gui_from_camera()
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select a render '
                                                   'camera in “Cam_02Render_Selection”!') + '\n')
            return

    ma.modifyAnimationIndicator(Animation = False)
    MC.Cam_02AnimCurrentStep = 0
    FreeCAD.Console.PrintMessage(translate('Movie', 'MovieCamera position A has been established.') + '\n')
    Gui.updateGui()

def setMCPosB(Option = None):

    MC = Option
    Gui.runCommand('Std_PerspectiveCamera',1)

    # Camera node position B
    cameraNodeB = Gui.ActiveDocument.ActiveView.getCameraNode()

    # Camera position B
    vectorNodeB = FreeCAD.Vector(cameraNodeB.position.getValue())
    MC.Cam_04XPosB = vectorNodeB[0]
    MC.Cam_05YPosB = vectorNodeB[1]
    MC.Cam_06ZPosB = vectorNodeB[2]

    # Camera angles pos B
    rotNodeB = FreeCAD.Rotation(*cameraNodeB.orientation.getValue().getValue())
    anglesYawPitchRollB = rotNodeB.getYawPitchRoll()
    MC.Cam_04YawPosB = anglesYawPitchRollB[0]
    MC.Cam_05PitchPosB = anglesYawPitchRollB[1]
    MC.Cam_06RollPosB = anglesYawPitchRollB[2]

    # Camera zoom pos B
    MC.Cam_03ZoomPosB = degrees(float(cameraNodeB.heightAngle.getValue()))

    # Render camera angles and zoom pos B
    if MC.Cam_01Type == 'Render':
        if 'Camera' in FreeCAD.ActiveDocument.Content and MC.Cam_02Render_Selection:
            renderCameraB = MC.Cam_02Render_Selection
            renderCameraB.ViewObject.Proxy.set_camera_from_gui()
            renderCameraB.AspectRatio = MC.Cam_03RenderWidth/MC.Cam_04RenderHeight
            renderCameraB.ViewportMapping = 'CROP_VIEWPORT_FILL_FRAME'
            renderCameraB.ViewObject.Proxy.set_gui_from_camera()
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select a render '
                                                   'camera in “Cam_02Render_Selection”!') + '\n')
            return

    ma.modifyAnimationIndicator(Animation = False)
    MC.Cam_02AnimCurrentStep = MC.Cam_04AnimTotalSteps
    FreeCAD.Console.PrintMessage(translate('Movie', 'MovieCamera position B has been established.') + '\n')
    Gui.updateGui()

# ======================================================================================

def getMovieCameraMobile(Selection = None):

    MC = Selection
    # Getting camera node
    cameraNode = Gui.ActiveDocument.ActiveView.getCameraNode()

    # Camera node follows route
    if MC.Cam_01Route == True:
        if not MC.Cam_02RouteSelection:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select '
                                                   'a route in “Cam_02RouteSelection”!') + '\n')
            ma.modifyAnimationIndicator(Animation = False)
            return

        route = MC.Cam_02RouteSelection.Shape.Edges[0]
        stepLength = route.Length/MC.Cam_04AnimTotalSteps
        currentStep = stepLength*MC.Cam_02AnimCurrentStep
        if currentStep > route.Length:
            currentStep = route.Length
        currentPos = route.getParameterByLength(currentStep)
        currentVector = route.valueAt(currentPos)
        cameraNode.position.setValue(currentVector)

        # Target follows the route
        if MC.Cam_01Target == 'Follow a route':

            lengthTarget  = currentStep + stepLength*MC.Cam_03TargetStepsForward
            posTarget = route.getParameterByLength(lengthTarget)
            vectorTarget = route.valueAt(posTarget)
            cameraTarget = (vectorTarget)
            cameraNode.pointAt(coin.SbVec3f(cameraTarget), coin.SbVec3f( 0, 0, 1 ) )

    # Camera node for Pos AB
    else:
        xPosCamera = MC.Cam_01XPosA
        yPosCamera = MC.Cam_02YPosA
        zPosCamera = MC.Cam_03ZPosA

        if MC.Cam_01XMov == True:
            xPosCameraInc = (MC.Cam_04XPosB - MC.Cam_01XPosA)/MC.Cam_04AnimTotalSteps
            xPosCamera = MC.Cam_01XPosA + xPosCameraInc*MC.Cam_02AnimCurrentStep
        if MC.Cam_02YMov == True:
            yPosCameraInc = (MC.Cam_05YPosB - MC.Cam_02YPosA)/MC.Cam_04AnimTotalSteps
            yPosCamera = MC.Cam_02YPosA + yPosCameraInc*MC.Cam_02AnimCurrentStep
        if MC.Cam_03ZMov == True:
            zPosCameraInc = (MC.Cam_06ZPosB - MC.Cam_03ZPosA)/MC.Cam_04AnimTotalSteps
            zPosCamera = MC.Cam_03ZPosA + zPosCameraInc*MC.Cam_02AnimCurrentStep

        cameraNode.position.setValue(xPosCamera, yPosCamera, zPosCamera)

    # Camera yaw, pitch and roll for Pos AB 
    if MC.Cam_01Target == 'Free':
        cameraYaw = MC.Cam_01YawPosA
        cameraPitch = MC.Cam_02PitchPosA
        cameraRoll = MC.Cam_03RollPosA

        if MC.Cam_01Yaw == True:
            yawInc = (MC.Cam_04YawPosB - MC.Cam_01YawPosA)/MC.Cam_04AnimTotalSteps
            cameraYaw = MC.Cam_01YawPosA + yawInc*MC.Cam_02AnimCurrentStep

        if MC.Cam_02Pitch == True:
            pitchInc = (MC.Cam_05PitchPosB - MC.Cam_02PitchPosA)/MC.Cam_04AnimTotalSteps
            cameraPitch = MC.Cam_02PitchPosA + pitchInc*MC.Cam_02AnimCurrentStep

        if MC.Cam_03Roll == True:
            rollInc = (MC.Cam_06RollPosB - MC.Cam_03RollPosA)/MC.Cam_04AnimTotalSteps
            cameraRoll = MC.Cam_03RollPosA + rollInc*MC.Cam_02AnimCurrentStep

        rotNode = FreeCAD.Rotation(*cameraNode.orientation.getValue().getValue())
        rotNode.setYawPitchRoll(cameraYaw, cameraPitch, cameraRoll)
        cameraNode.orientation.setValue(rotNode.Q)

    # Camera Pos AB zoom
    if MC.Cam_04Zoom == True:
        zoomCameraInc = (MC.Cam_03ZoomPosB - MC.Cam_02ZoomPosA)/MC.Cam_04AnimTotalSteps
        cameraHeightAngle = MC.Cam_02ZoomPosA + zoomCameraInc*MC.Cam_02AnimCurrentStep
        cameraNode.heightAngle.setValue(radians(float(cameraHeightAngle)))

    # Object or point target
    if MC.Cam_01Target == 'Follow an object or point':
        if not MC.Cam_02TargetObjectSelection:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select an '
                                                   'object or point in “Cam_02TargetObjectSelection”!') + '\n')
            ma.modifyAnimationIndicator(Animation = False)
            return

        cameraFixedTarget = MC.Cam_02TargetObjectSelection.Placement.Base
        cameraNode.pointAt( coin.SbVec3f(cameraFixedTarget), coin.SbVec3f( 0, 0, 1 ) )

    #  Render camera
    if MC.Cam_01Type == 'Render':
        if not MC.Cam_02Render_Selection:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select '
                                                   'a render camera in “Cam_02Render_Selection”!') + '\n')
            ma.modifyAnimationIndicator(Animation = False)
            return

        renderCamera = MC.Cam_02Render_Selection
        renderCamera.ViewObject.Proxy.set_camera_from_gui()

        if MC.Cam_01Route == True:
            renderCamera.AspectRatio = MC.Cam_03RenderWidth/MC.Cam_04RenderHeight
            renderCamera.ViewportMapping = 'CROP_VIEWPORT_FILL_FRAME'

        renderCamera.ViewObject.Proxy.set_gui_from_camera()

# ======================================================================================

# 3. Commands

if FreeCAD.GuiUp:
    FreeCAD.Gui.addCommand('CreateMovieCamera', CreateMovieCamera())
    FreeCAD.Gui.addCommand('EnableMovieCamera', EnableMovieCamera())

# ======================================================================================
