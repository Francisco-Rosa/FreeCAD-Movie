''' Movie Workbench, Movie Object animation module '''

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
import time
import os
from math import degrees, radians
from PySide.QtCore import QT_TRANSLATE_NOOP
import RecordPlayVideo as rpv
import MovieCamera as mc

translate = FreeCAD.Qt.translate

LanguagePath = os.path.dirname(__file__) + '/translations'
Gui.addLanguagePath(LanguagePath)

# ======================================================================================
# 0. Global

STEP_POS = 'I'
MO = None
CL_PRESENCE = False
OBJECTS = []

def verification():
    global CL_PRESENCE
    if 'Clapperboard' in FreeCAD.ActiveDocument.Content:
        CL_PRESENCE = True
    else:
        CL_PRESENCE = False

# ======================================================================================
# 1. Classes

class MovieObjects:
    '''Class to create a group of objects to be animated'''

    def __init__(self, obj):
        obj.addProperty('App::PropertyLinkList', 'Objects', 'Movie Objects', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Select or choose the objects you want to animate.'
                                                    )).Objects = []
        obj.addProperty('App::PropertyPythonObject', 'Names').Names = []
        obj.addProperty('App::PropertyPythonObject', 'CenterGravityA').CenterGravityA = {}
        obj.addProperty('App::PropertyPythonObject', 'CenterGravityB').CenterGravityB = {}
        obj.addProperty('App::PropertyPythonObject', 'Pos0').Pos0 = {} # Placement0
        obj.addProperty('App::PropertyPythonObject', 'PosA').PosA = {} # PlacementA
        obj.addProperty('App::PropertyPythonObject', 'PosB').PosB = {} # PlacementB
        obj.addProperty('App::PropertyPythonObject', 'ObjectAxis').ObjectAxis = {}
        obj.addProperty('App::PropertyPythonObject', 'PosGCAverage0').PosGCAverage0 = []

    # Movie Objects 01 - Animation config 

        obj.addProperty('App::PropertyInteger', 'Anim_1TotalSteps', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Indicate the number of steps through which the objects will be '
                                                    'animate in this section.')).Anim_1TotalSteps = 50
        obj.addProperty('App::PropertyInteger', 'Anim_2IniStep', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Indicate the step which this section of the animation will begin.')).Anim_2IniStep = 0
        obj.addProperty('App::PropertyInteger', 'Anim_3EndStep', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Indicate the step which this section of the animation will finish.')).Anim_3EndStep = 50
        obj.addProperty('App::PropertyInteger', 'Anim_4CurrentStep', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'The current step of this section of the animation.')).Anim_4CurrentStep = 0
        obj.addProperty('App::PropertyInteger', 'Anim_5Fps', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Indicate the fps through the section of the animation will be '
                                                    'performed. It is a simulation and will depend on the '
                                                    'computer performance.')).Anim_5Fps = 30
        obj.addProperty('App::PropertyBool', 'Anim_6OnAnim', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                     'It only indicative whether the objects are in animation or not. '
                                                     'It should not be changed manually, it is controlled by the animations buttons.'
                                                     )).Anim_6OnAnim = False

    # Movie Objects 02 - Objects follows a path

        obj.addProperty('App::PropertyBool', 'Objects_Route', 'Movie Objects 02 - Objects follows a path', 
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Choose True if the objects will follow a route. '
                                                    'You have to select a single segment on Objects_Route_Selection to use it.'
                                                    )).Objects_Route = False
        obj.addProperty('App::PropertyLink', 'Objects_Route_Selection', 'Movie Objects 02 - Objects follows a path', 
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Choose the route through which the objects will be '
                                                    'animate. You have to select a single segment such as: line, arc, circle, '
                                                    'ellipse, B-spline or Bézier curve, from Sketcher or Draft Workbenches.'
                                                    )).Objects_Route_Selection = None

    # Movie Objects 03 - Objects rotation
        obj.addProperty('App::PropertyBool', 'Objects_Rotation', 'Movie Objects 03 - Objects rotation', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Choose True, if you want '
                                                    'animate the object angles.')).Objects_Rotation = False
        obj.addProperty('App::PropertyBool', 'Objects_RotationCG', 'Movie Objects 03 - Objects rotation', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Choose True, if you want '
                                                    'rotate the objects by their centers of gravity.')).Objects_RotationCG = False

        obj.Proxy = self

class MovieObjectsViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/MovieObjectsIcon.svg'

# ======================================================================================
# 2. Command classes

class CreateMovieObjects:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/CreateMovieObjectsIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('CreateMovieObjects', 'Create a Movie Objects'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateMovieObjects', 
                                             'Create a group of objects that goes from position '
                                             'A to B, follows a route or rotate around a chosen axis.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            return True

        else:
            return False

    def Activated(self):
        global MO
        listObjects = []
        listObjects = Gui.Selection.getSelection()
        if not listObjects:
            FreeCAD.Console.PrintMessage(translate('Movie', 'Select at least one '
                                                   'object to create a Movie Objects') + '\n')
            return
        else:
            Gui.Selection.clearSelection()
            # Objects original positions and angles
            ActivatedMovieObjects(self)
            MO.Objects = listObjects
            sumGC = FreeCAD.Vector(0,0,0)

            for n in range(len(listObjects)):
                Object = listObjects[n]
                name = Object.Name
                MO.Names.append(name)
                MO.ObjectAxis[name] = 'None' # Apply no external rotation axis to object
                vectorCenterGravity0 = listObjects[n].Shape.CenterOfGravity
                sumGC = sumGC + vectorCenterGravity0
                vectorBase0 = listObjects[n].Placement.Base
                coordBase0 = (vectorBase0[0], vectorBase0[1], vectorBase0[2])
                rotation0 = listObjects[n].Placement.Rotation.getYawPitchRoll()
                placement0 = (coordBase0, rotation0)
                MO.Pos0[name] = placement0

            # Initial vector of gravity centers average
            vectorGCAverage0 = sumGC/len(listObjects)
            MO.PosGCAverage0 = (vectorGCAverage0[0], vectorGCAverage0[1], vectorGCAverage0[2])
            mc.modifyAnimationIndicator(Animation = False)
            MO.Anim_6OnAnim = False

def ActivatedMovieObjects(self):
    global MO
    folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'MovieObjects')
    MovieObjects(folder)
    MovieObjectsViewProvider(folder.ViewObject)
    MO = folder

# ======================================================================================

class EnableMovieObjects:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/EnableMovieObjectsIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('EnableMovieObjects', 'Enable one or more select movie objects'),
                'ToolTip': QT_TRANSLATE_NOOP('EnableMovieObjects',
                                             'Select the movie objects that you want to configure, '
                                             'then click on this button to enable to be possible to configure '
                                             'the pos A and B. After that, '
                                             'enable the connection with a Movie Camera in Objects_3Connection.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            return True

        else:
            return False

    def Activated(self):
        enableMovieObjects(Enable = 'Objects')

def enableMovieObjects(Enable = 'None'):
    global MO
    global NO
    global OBJECTS

    OBJECTS = []
    if Enable == 'Objects':
        OBJECTS = Gui.Selection.getSelection()
        if not OBJECTS:
            FreeCAD.Console.PrintMessage(translate('Movie', 'Select a '
                                                   'Movie Object to configure') + '\n')
            return
        else:
            mc.enableCameraObjects(Enable = 'Objects')
            Gui.Selection.clearSelection()
            verification()
            mc.modifyAnimationIndicator(Animation = False)

    if Enable == 'Camera and objects':
        from MovieCamera import MC
        OBJECTS = MC.Cam_5ObjectsSelected
    NO = 0
    MO = OBJECTS[NO]
    MO.Anim_6OnAnim = False

# ======================================================================================

class ExcludeMovieObjects:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/ExcludeMovieObjectsIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('ExcludeMovieObjects', 'Exclude a select movie objects'),
                'ToolTip': QT_TRANSLATE_NOOP('ExcludeMovieObjects', 
                                             'Select a movie objects that you want to exclude, '
                                             'then click on this button. The objects positions and '
                                             'angles will be reset to the initial values')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not MO.Anim_6OnAnim:
                return True

        else:
            return False

    def Activated(self):
        excludeMovieObjects()

def excludeMovieObjects():
    global MO
    selection = []
    selection = Gui.Selection.getSelection()
    if not selection:
        FreeCAD.Console.PrintMessage(translate('Movie', 'Select a '
                                                   'Movie Object to exclude') + '\n')
        return
    else:
        MO = selection[0]
        MO.PosA = MO.Pos0
        MO.PosB = MO.Pos0
        getMovieObjectsMobile()
        MO = []
        Gui.runCommand('Std_Delete',0)

# ======================================================================================

class SetMovieObjectsAxis:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/SetMovieObjectsAxisIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('SetMovieObjectsAxis', 'Set an axis to objects'),
                'ToolTip': QT_TRANSLATE_NOOP('SetMovieObjectsAxis', 
                                             'After create a MovieObjects, Pos A and B set, select those '
                                             'objects you want to rotate around a axis. '
                                             'Select first the objects, then the axis. '
                                             'To erase these settings, click on SetMoviePosB button' )}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not MO.Anim_6OnAnim:
                return True

        else:
            return False

    def Activated(self):
        setObjectsAxis()
# ======================================================================================  
# 3. Functions

def setMOPosA():

    global MO
    global STEP_POS

    # Objects position and angles A
    for n in range(len(MO.Names)):
        name = MO.Names[n]
        vectorCGA = MO.Objects[n].Shape.CenterOfGravity
        coordCGA = (vectorCGA[0], vectorCGA[1], vectorCGA[2])
        MO.CenterGravityA[name] = coordCGA
        vectorBaseA = MO.Objects[n].Placement.Base
        coordBaseA = (vectorBaseA[0], vectorBaseA[1], vectorBaseA[2])
        rotationA = MO.Objects[n].Placement.Rotation.getYawPitchRoll()
        placementA = (coordBaseA, rotationA)
        MO.PosA[name] = placementA

    MO.Anim_4CurrentStep = 0
    mc.modifyAnimationIndicator(Animation = False)
    MO.Anim_6OnAnim = False
    MO.Objects_Rotation = True
    STEP_POS = 'I'
    Gui.updateGui()

def setMOPosB():

    global MO
    global STEP_POS

    # Objects position and angles B
    MO.ObjectAxis = {} #Delete any config. of previous setMovieObjectsAxis

    for n in range(len(MO.Names)):
        name = MO.Names[n]
        MO.ObjectAxis[name] = 'None' # Delete any previous external rotation axis to object
        vectorCGB = MO.Objects[n].Shape.CenterOfGravity
        coordCGB = (vectorCGB[0], vectorCGB[1], vectorCGB[2])
        MO.CenterGravityB[name] = coordCGB
        vectorBaseB = MO.Objects[n].Placement.Base
        coordBaseB = (vectorBaseB[0], vectorBaseB[1], vectorBaseB[2])
        rotationB = MO.Objects[n].Placement.Rotation.getYawPitchRoll()
        placementB = (coordBaseB, rotationB)
        MO.PosB[name] = placementB

    MO.Anim_4CurrentStep = MO.Anim_1TotalSteps
    mc.modifyAnimationIndicator(Animation = False)
    MO.Anim_6OnAnim = False
    MO.Objects_Rotation = True
    STEP_POS = 'I'
    Gui.updateGui()

def setObjectsAxis():
    global MO
    listObjects = []
    listObjects = Gui.Selection.getSelection()
    if not listObjects:
        FreeCAD.Console.PrintMessage(translate('Movie', 'First select the objects '
                                               'you want to rotate then the axis of rotation ') + '\n')
        return
    else:
        Gui.Selection.clearSelection()
        #Last object selected must be the axis
        Object = listObjects[-1]
        AxisName = Object.Name
        # Set an external rotation axis to object
        for n in range(len(listObjects)):
            Object = listObjects[n]
            name = Object.Name
            if name != AxisName:
                MO.ObjectAxis[name] = AxisName

    mc.modifyAnimationIndicator(Animation = False)
    MO.Anim_6OnAnim = False

def recoverIniMovieObjects():
    global STEP_POS
    global NO
    global OBJECTS
    global MO

    if MO.Anim_4CurrentStep - MO.Anim_2IniStep > 0:
        MO.Anim_4CurrentStep = MO.Anim_2IniStep

    else:
        nextMovieObjects(condition = 'back')

    STEP_POS = 'I'
    getMovieObjectsMobile()
    Gui.updateGui()

def prevMovieObjects():
    global MO
    if MO.Anim_4CurrentStep - MO.Anim_2IniStep > 0:
        MO.Anim_4CurrentStep -= 1
    else:
        nextMovieObjects(condition = 'back')

    getMovieObjectsMobile()
    Gui.updateGui()

def pauseMovieObjects():
    global MO
    MO.Anim_6OnAnim = False
    mc.modifyAnimationIndicator(Animation = False)

def playMovieObjects():

    global NO
    global STEP_POS
    global MO

    leftObjects = len(OBJECTS) - NO

    for o in range(leftObjects):
        MO = OBJECTS[NO]
        Gui.Selection.addSelection(MO)
        pauseTime = MO.Anim_1TotalSteps/(MO.Anim_5Fps*1000) # meter (*1000)
        MO.Anim_6OnAnim = True
        mc.modifyAnimationIndicator(Animation = True)
        FreeCAD.ActiveDocument.recompute()
        if STEP_POS == 'I':
            MO.Anim_4CurrentStep = MO.Anim_2IniStep

        steps = MO.Anim_3EndStep - MO.Anim_4CurrentStep

        STEP_POS = 'P'

        for p in range (steps+1):

            getMovieObjectsMobile()
            Gui.updateGui()
            time.sleep(pauseTime)

            if CL_PRESENCE == True:
                CL = FreeCAD.ActiveDocument.Clapperboard
                if CL.Cam_3OnRec == True:
                    rpv.runRecordCamera()

            if MO.Anim_6OnAnim == False:
                break

            MO.Anim_4CurrentStep += 1

        if MO.Anim_6OnAnim == False:
            break

        Gui.Selection.clearSelection()
        mc.modifyAnimationIndicator(Animation = False)
        MO.Anim_6OnAnim = False
        if o < (leftObjects - 1):
            NO += 1

    if CL_PRESENCE == True:
        CL = FreeCAD.ActiveDocument.Clapperboard
        CL.Cam_3OnRec = False

def getMovieObjectsMobile():

    # Objects Pos AB yaw, pitch and roll
    if MO.Objects_Rotation == True:

        for n in range(len(MO.Objects)):
            # Object yaw, pitch and roll pos A and posB
            name = MO.Names[n] 
            anglesAn = MO.PosA[name][1]
            anglesBn = MO.PosB[name][1]

            # Object rotate one step (anglesB_Objects - anglesA_Objects)
            def getIncAngle(angleA = 0, angleB = 0):
                if angleB - angleA <= 180:
                    IncAngleStep = (angleB - angleA)/MO.Anim_1TotalSteps
                else:
                    IncAngleStep = (angleB - angleA - 360)/MO.Anim_1TotalSteps
                IncAngle1 = IncAngleStep*MO.Anim_4CurrentStep
                return IncAngle1

            yawObjectn1 = getIncAngle(angleA = anglesAn[0], angleB = anglesBn[0])
            yawObjectn2 = anglesAn[0] + yawObjectn1

            pitchObjectn1 = getIncAngle(angleA = anglesAn[1], angleB = anglesBn[1])
            pitchObjectn2 = anglesAn[1] + pitchObjectn1

            rollObjectn1 = getIncAngle(angleA = anglesAn[2], angleB = anglesBn[2])
            rollObjectn2 = anglesAn[2] + rollObjectn1
 
            # Object Rotates around a chosen axis
            if MO.ObjectAxis[name] != 'None':
                # Reset to the PosA
                vectorA = FreeCAD.Base.Vector(MO.PosA[name][0])
                MO.Objects[n].Placement.Base = vectorA
                MO.Objects[n].Placement.Rotation.setYawPitchRoll(anglesAn[0], anglesAn[1], anglesAn[2])
                # Placement with base, rotation and axis:
                objRot = FreeCAD.Base.Rotation(yawObjectn1, pitchObjectn1, rollObjectn1)
                axisObject = FreeCAD.ActiveDocument.getObject(MO.ObjectAxis[name])
                objBase = axisObject.Placement.Rotation.Axis
                centerRot = axisObject.Placement.Base
                placement = FreeCAD.Placement(objBase, objRot, centerRot)
                MO.Objects[n].Placement = placement.multiply(MO.Objects[n].Placement)

            # Object Rotates without a chosen axis
            else:
                MO.Objects[n].Placement.Rotation.setYawPitchRoll(yawObjectn2, pitchObjectn2, rollObjectn2)

    # Object that follows a route moves one step
    if MO.Objects_Route == True:
        if not MO.Objects_Route_Selection:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select '
                                                   'a route in Objects_Route_Selection') + '\n')
            MO.Anim_6OnAnim = False
            mc.modifyAnimationIndicator(Animation = False)
            return
        # Calculating the current vector on the route
        route = MO.Objects_Route_Selection.Shape.Edges[0]
        stepLength = route.Length/MO.Anim_1TotalSteps
        currentStep = stepLength*MO.Anim_4CurrentStep
        currentPos = route.getParameterByLength(currentStep)
        currentVector = route.valueAt(currentPos)

        # Transferring the position to the bases of the objects
        for n in range(len(MO.Names)):
            name = MO.Names[n]
            VectorCGAverage = FreeCAD.Vector(MO.PosGCAverage0)
            # The gap1, difference between the average of the centers of gravities and the object's Pos0
            gap1 = VectorCGAverage - FreeCAD.Vector(MO.Pos0[name][0])
            # The average of the centers of gravities receives the values of current vector
            VectorCGAverage = currentVector
            # The base of object is the difference between current vector and the gap1
            vector = VectorCGAverage - gap1
            MO.Objects[n].Placement.Base = vector
    else:
        # Object moves one step (PosA - PosB)
        for n in range(len(MO.Names)):
            name = MO.Names[n]
            # Only the objects without a chosen axis
            if MO.ObjectAxis[name] == 'None':
                # Moving through the bases of objects
                if MO.Objects_RotationCG == False:
                    vectorA = FreeCAD.Vector(MO.PosA[name][0])
                    vectorB = FreeCAD.Vector(MO.PosB[name][0])
                    vectorInc = (vectorB - vectorA)/MO.Anim_1TotalSteps
                    vector = vectorA + vectorInc*MO.Anim_4CurrentStep
                    MO.Objects[n].Placement.Base = vector
                # Moving through objects' centers of gravity
                else:
                    # The current vector will be the center of gravity
                    CGA = FreeCAD.Vector(MO.CenterGravityA[name])
                    CGB = FreeCAD.Vector(MO.CenterGravityB[name])
                    CGInc = (CGB - CGA)/MO.Anim_1TotalSteps
                    CG = CGA + CGInc*MO.Anim_4CurrentStep
                    currentVector = CG
                    # Transferring the position to the base of the object
                    # The gap2, difference between the center of gravity and the object's base
                    gap2 = MO.Objects[n].Shape.CenterOfGravity - MO.Objects[n].Placement.Base
                    # The base of object will be the difference between the center of gravity and the gap2
                    vector = CG - gap2
                    MO.Objects[n].Placement.Base = vector

def nextMovieObjects(condition = 'none'):
    global NO
    global OBJECTS
    global MO

    # Goes back a group of objects and move one step back, if so
    if condition == 'back':
        if NO> 0:
            NO -= 1
            MO = OBJECTS[NO]
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(MO)
            MO.Anim_4CurrentStep = MO.Anim_3EndStep
        else:
            mc.nextMovieCamera(condition = 'back')
            return

    # Advances and plays the next animation of a group of objects, if so
    if condition == 'next1' or condition == 'next2':
        if NO < (len(OBJECTS)- 1):
            NO += 1
            MO = OBJECTS[NO]
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(MO)
            STEP_POS = 'I'
            if condition == 'next2':
                MO.Anim_6OnAnim = False
                mc.modifyAnimationIndicator(Animation = False)
        else:
            if condition == 'next2':
                mc.nextMovieCamera(condition = 'next')
                mc.enableCameraObjects(Enable = 'None')
            return

def postMovieObjects(Enable = None):

    global NO
    global STEP_POS
    global MO

    if MO.Anim_3EndStep - MO.Anim_4CurrentStep > 0:
        MO.Anim_4CurrentStep += 1
    else:
        nextMovieObjects(condition = 'next1')
        if Enable == 'Objects':
            MO.Anim_6OnAnim = False
            mc.modifyAnimationIndicator(Animation = False)
            playMovieObjects()
        else:
            getMovieObjectsMobile()

    getMovieObjectsMobile()
    Gui.updateGui()

def getEndMovieObjects():

    global NO
    global STEP_POS
    global MO

    if MO.Anim_3EndStep - MO.Anim_4CurrentStep > 0:
        MO.Anim_4CurrentStep = MO.Anim_3EndStep
    else:
        nextMovieObjects(condition = 'next2')

    getMovieObjectsMobile()
    Gui.updateGui()

# ======================================================================================

# 3. Commands

if FreeCAD.GuiUp:
    FreeCAD.Gui.addCommand('CreateMovieObjects', CreateMovieObjects())
    FreeCAD.Gui.addCommand('EnableMovieObjects', EnableMovieObjects())
    FreeCAD.Gui.addCommand('ExcludeMovieObjects', ExcludeMovieObjects())
    FreeCAD.Gui.addCommand('SetMovieObjectsAxis', SetMovieObjectsAxis())

# ======================================================================================
