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
import os
import time
from math import degrees, radians
from PySide.QtCore import QT_TRANSLATE_NOOP
import MovieAnimation as ma

translate = FreeCAD.Qt.translate

LanguagePath = os.path.dirname(__file__) + '/translations'
Gui.addLanguagePath(LanguagePath)

# ======================================================================================
# 0. Global

MO = None

def enableObjectsSelection(Enable = None):
    global MO
    MO = Enable
    # New - Updating PosA and PosB
    #if(hasattr(MO, 'PosAList')):
    if hasattr(MO, 'PosAList'):
        import ast
        if MO.PosAList != []:
            MO.PosA = ast.literal_eval(MO.PosAList[0])
        if MO.PosBList != []:
            MO.PosB = ast.literal_eval(MO.PosBList[0])

# Refreshes each step of objects animation
OBJ_REFRESH = False
def enableObjectsRefresh(Enable = False):
    global OBJ_REFRESH
    if Enable == True:
        OBJ_REFRESH = True
    else:
        OBJ_REFRESH = False

# ======================================================================================
# 1. Classes

class MovieObjects:
    '''Class to create a group of objects to be animated'''

    def __init__(self, obj):
        obj.addProperty('App::PropertyLinkList', 'Objects', 'Movie Objects', QT_TRANSLATE_NOOP('App::Property', 
                                                    'List of objects of this MovieObjects.'
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


        obj.addProperty('App::PropertyInteger', 'Obj_01AnimIniStep', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Initial step of the MovieObjects animation. Indicate the step which this section of the '
                                                    'animation will begin. Changes will only take '
                                                    'effect after MovieObjects has been re-enabled.')).Obj_01AnimIniStep = 0
        obj.addProperty('App::PropertyInteger', 'Obj_02AnimCurrentStep', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Current step of the MovieObjects animation. It is only indicative.'
                                                    )).Obj_02AnimCurrentStep = 0
        obj.addProperty('App::PropertyInteger', 'Obj_03AnimEndStep', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'End step of the MovieObjects animation. Indicate the step which this section of the animation '
                                                    'will finish. Changes will only take '
                                                    'effect after MovieObjects has been re-enabled.')).Obj_03AnimEndStep = 50
        obj.addProperty('App::PropertyInteger', 'Obj_04AnimTotalSteps', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Total steps of MovieObjects animation. It is the result of the difference between End step '
                                                    '(“Obj_03AnimEndStep“) and Initial step (“Obj_01AnimIniStep“).'
                                                    )).Obj_04AnimTotalSteps = 50
        obj.addProperty('App::PropertyInteger', 'Obj_05AnimFps', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Animation fps of the MovieObjects. Indicate the fps through which the section of the animation '
                                                    'will be '
                                                    'performed. It is a simulation and will depend on the '
                                                    'computer performance. Changes will only take '
                                                    'effect after MovieObjects has been re-enabled.')).Obj_05AnimFps = 30
        obj.addProperty('App::PropertyString', 'Obj_06AnimTime', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Animation time of the MovieObjects, in in hours, minutes, and seconds. '
                                                    'It is only indicative.'
                                                    )).Obj_06AnimTime = time.strftime("%H:%M:%S", time.gmtime(1.7))
        obj.addProperty('App::PropertyBool', 'Obj_07AnimOnAnim', 'Movie Objects 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                     'MovieObjects animation on or off. '
                                                     'It should not be changed manually, it is controlled by the animation buttons.'
                                                     )).Obj_07AnimOnAnim = False

    # Movie Objects 02 - Objects config

        obj.addProperty('App::PropertyBool', 'Obj_01Route', 'Movie Objects 02 - Objects config', 
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Route of the MovieObjects. Choose “true” if the objects follow a route. '
                                                    'You have to select a single segment on Route selection (“Obj_02RouteSelection“) to use it. '
                                                    'With the route activated, the coordinate settings for points A and B will be ignored, but not deleted. '
                                                    'Disable the route and the animation of points A and B will be activated again, if it has already been '
                                                    'configured before.'
                                                    )).Obj_01Route = False
        obj.addProperty('App::PropertyLink', 'Obj_02RouteSelection', 'Movie Objects 02 - Objects config', 
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Route selection of the MovieObjects. Choose the route through which the objects will be '
                                                    'animate. You have to select a single segment such as: line, arc, circle, '
                                                    'ellipse, B-spline or Bézier curve, from Sketcher or Draft Workbenches.'
                                                    )).Obj_02RouteSelection = None

    # Movie Objects 03 - Objects rotation
        obj.addProperty('App::PropertyBool', 'Obj_01Rotation', 'Movie Objects 03 - Objects rotation', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Rotation of the MovieObjects. Choose “true”, if you want to '
                                                    'animate the objects angles.')).Obj_01Rotation = False
        obj.addProperty('App::PropertyBool', 'Obj_02RotationCG', 'Movie Objects 03 - Objects rotation', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Rotation by the centers of gravities of the MovieObjects. Choose '
                                                    '“true”, if you want to rotate the objects by their '
                                                    'centers of gravity.')).Obj_02RotationCG = False

        obj.Proxy = self

    # New properties
    #def updateProps(self, obj):
        obj.addProperty('App::PropertyStringList', 'PosAList', 'Movie Objects', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Placements of PosA of this MovieObjects.'
                                                    )).PosAList = [] # New
        obj.addProperty('App::PropertyStringList', 'PosBList', 'Movie Objects', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Placements of PosB of this MovieObjects.'
                                                    )).PosBList = [] # New
        obj.addProperty('App::PropertyBool', 'Obj_03Refresh', 'Movie Objects 02 - Objects config', 
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Refresh on or off. Choose “true” if you need to update at each '
                                                    'step of the animation. Sometimes needed in combination with other object animation '
                                                    'workbenches. Note: This decreases the performance of object animations.'
                                                    )).Obj_03Refresh = False

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
                'MenuText': QT_TRANSLATE_NOOP('CreateMovieObjects', 'MovieObjects'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateMovieObjects', 
                                             'First select a group of objects you want to animate and '
                                             'click here. Objects can move from position A to B, '
                                             'follow a route, rotate around their gravity centers or a chosen axis.')}

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
                                                   'object to create a MovieObjects!') + '\n')
            return
        else:
            Gui.Selection.clearSelection()
            # Objects initial positions and angles
            ActivatedMovieObjects(self)
            MO.Objects = listObjects
            sumCG = FreeCAD.Vector(0,0,0)

            for n in range(len(listObjects)):
                Object = listObjects[n]
                name = Object.Name
                MO.Names.append(name)
                MO.ObjectAxis[name] = 'None' # Apply no external rotation axis to object
                vectorCenterGravity0 = listObjects[n].Shape.CenterOfGravity
                sumCG = sumCG + vectorCenterGravity0
                vectorBase0 = listObjects[n].Placement.Base
                coordBase0 = (vectorBase0[0], vectorBase0[1], vectorBase0[2])
                rotation0 = listObjects[n].Placement.Rotation.getYawPitchRoll()
                placement0 = (coordBase0, rotation0)
                MO.Pos0[name] = placement0

            # Initial vector of gravity centers average
            vectorGCAverage0 = sumCG/len(listObjects)
            MO.PosGCAverage0 = (vectorGCAverage0[0], vectorGCAverage0[1], vectorGCAverage0[2])
            ma.modifyAnimationIndicator(Animation = False)

def ActivatedMovieObjects(self):
    global MO

    default_label = translate('Movie', 'MovieObjects')
    folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'MovieObjects')
    MovieObjects(folder)
    MovieObjectsViewProvider(folder.ViewObject)
    MO = folder
    MO.Label = default_label

class EnableMovieObjects:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/EnableMovieObjectsIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('EnableMovieObjects', 'Enable a MovieObjects'),
                'ToolTip': QT_TRANSLATE_NOOP('EnableMovieObjects',
                                             'Select the MovieObjects that you want to configure, '
                                             'then click on this button to be possible to configure '
                                             'its positions A and B, set an axis or exclude it.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        ma.enableMovieSelection(Enable = 'Objects')

class SetMovieObjectsAxis:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/SetMovieObjectsAxisIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('SetMovieObjectsAxis', 'Set an axis'),
                'ToolTip': QT_TRANSLATE_NOOP('SetMovieObjectsAxis', 
                                             'After create a MovieObjects, position A and B set, select those '
                                             'objects you want to rotate around a axis. '
                                             'Select first the objects, then the axis. '
                                             'To erase these settings, click on Set position B button.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not MO.Obj_07AnimOnAnim:
                return True
        else:
            return False

    def Activated(self):
        setObjectsAxis(Option = MO)

class ExcludeMovieObjects:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/ExcludeMovieObjectsIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('ExcludeMovieObjects', 'Exclude a MovieObjects'),
                'ToolTip': QT_TRANSLATE_NOOP('ExcludeMovieObjects', 
                                             'Select a MovieObjects that you want to exclude, '
                                             'then click on this button. Objects positions and angles '
                                             'will revert to the values set when the MovieObjects were created.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not MO.Obj_07AnimOnAnim:
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
                                                   'MovieObjects to exclude!') + '\n')
        return
    else:
        MO = selection[0]
        MO.PosA = MO.Pos0
        MO.PosB = MO.Pos0
        getMovieObjectsMobile(Selection = MO)
        MO = []
        Gui.runCommand('Std_Delete',0)

# ======================================================================================
# 3. Functions

def setMOPosA(Option = None):

    MO = Option

    # PosA - positions, angles and centers of gravity of objects
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

    MO.Obj_02AnimCurrentStep = 0
    ma.modifyAnimationIndicator(Animation = False)
    MO.Obj_01Rotation = True
    FreeCAD.Console.PrintMessage(translate('Movie', 'MovieObjects position A has been established.') + '\n')
    if(hasattr(MO, 'PosAList')): # New
        MO.PosAList = str(MO.PosA) # New
    Gui.updateGui()

def setMOPosB(Option = None):

    MO = Option

    # PosB - positions, angles and centers of gravity of objects
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

    MO.Obj_02AnimCurrentStep = MO.Obj_04AnimTotalSteps
    ma.modifyAnimationIndicator(Animation = False)
    MO.Obj_01Rotation = True
    FreeCAD.Console.PrintMessage(translate('Movie', 'MovieObjects position B has been established.') + '\n')
    if(hasattr(MO, 'PosBList')): # New
        MO.PosBList = str(MO.PosB) # New
    Gui.updateGui()

def setObjectsAxis(Option = None):
    MO = Option
    listObjects = []
    listObjects = Gui.Selection.getSelection()
    if not listObjects:
        FreeCAD.Console.PrintMessage(translate('Movie', 'First select the objects '
                                               'you want to rotate then the axis of rotation.') + '\n')
        return
    else:
        Gui.Selection.clearSelection()
        # Last object selected will be the axis
        Object = listObjects[-1]
        AxisName = Object.Name
        # Set the external rotation axis to each object
        for n in range(len(listObjects)):
            Object = listObjects[n]
            name = Object.Name
            if name != AxisName:
                MO.ObjectAxis[name] = AxisName

    ma.modifyAnimationIndicator(Animation = False)

def getMovieObjectsMobile(Selection = None):
    global OBJ_REFRESH
    MO = Selection

    # Objects Pos AB - Angles: yaw, pitch and roll
    if MO.Obj_01Rotation == True:

        for n in range(len(MO.Objects)):
            name = MO.Names[n]
            anglesAn = MO.PosA[name][1]
            anglesBn = MO.PosB[name][1]

            # Object rotate one step
            def getIncAngle(angleA = 0, angleB = 0):
                #New
                IncAngleStep = (angleB - angleA)/MO.Obj_04AnimTotalSteps
                IncAngle1 = IncAngleStep*MO.Obj_02AnimCurrentStep
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
                axisObject = FreeCAD.ActiveDocument.getObject(MO.ObjectAxis[name])
                objBase = axisObject.Placement.Rotation.Axis
                objRot = FreeCAD.Base.Rotation(yawObjectn1, pitchObjectn1, rollObjectn1)
                centerRot = axisObject.Placement.Base
                placement = FreeCAD.Placement(objBase, objRot, centerRot)
                MO.Objects[n].Placement = placement.multiply(MO.Objects[n].Placement)

            # Object Rotates without a chosen axis
            else:
                MO.Objects[n].Placement.Rotation.setYawPitchRoll(yawObjectn2, pitchObjectn2, rollObjectn2)

    # Objects that follow a route
    if MO.Obj_01Route == True:
        if not MO.Obj_02RouteSelection:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select '
                                                   'a route in “Obj_02RouteSelection“!') + '\n')
            ma.modifyAnimationIndicator(Animation = False)
            return
        # Calculating the current vector on the route
        route = MO.Obj_02RouteSelection.Shape.Edges[0]
        stepLength = route.Length/MO.Obj_04AnimTotalSteps
        currentStep = stepLength*MO.Obj_02AnimCurrentStep
        if currentStep > route.Length:
            currentStep = route.Length
        currentPos = route.getParameterByLength(currentStep)
        currentVector = route.valueAt(currentPos)

        # Transferring the route position to the bases of the objects or there centers of gravity
        # (through the average of the centers of gravity)
        VectorCGAverageXY = FreeCAD.Vector(MO.PosGCAverage0[0], MO.PosGCAverage0[1], 0)
        for n in range(len(MO.Names)):
            name = MO.Names[n]     
            # The gap1, difference between the average of the centers of gravity and the object's Pos0
            gap1 = VectorCGAverageXY - FreeCAD.Vector(MO.Pos0[name][0])
            # 1. Moving through the bases of objects:
            # The base of each object is the difference between current vector and the gap1
            vector = currentVector - gap1
            # 2. Moving through objects' centers of gravity:
            # The difference between the current center of gravity and the object's base
            gap2 = MO.Objects[n].Shape.CenterOfGravity - MO.Objects[n].Placement.Base
            # The base of object will be the difference between the center of gravity and the gap2
            vector = vector - gap2
            MO.Objects[n].Placement.Base = vector
    else:
        # Objects move one step (PosA - PosB)
        for n in range(len(MO.Names)):
            name = MO.Names[n]
            # Only the objects without a chosen axis
            if MO.ObjectAxis[name] == 'None':
                # Moving through the bases of objects
                if MO.Obj_02RotationCG == False:
                    vectorA = FreeCAD.Vector(MO.PosA[name][0])
                    vectorB = FreeCAD.Vector(MO.PosB[name][0])
                    vectorInc = (vectorB - vectorA)/MO.Obj_04AnimTotalSteps
                    vector = vectorA + vectorInc*MO.Obj_02AnimCurrentStep
                    MO.Objects[n].Placement.Base = vector
                # Moving through objects' centers of gravity
                else:
                    # The position of the center of gravity of each object
                    CGA = FreeCAD.Vector(MO.CenterGravityA[name])
                    CGB = FreeCAD.Vector(MO.CenterGravityB[name])
                    CGInc = (CGB - CGA)/MO.Obj_04AnimTotalSteps
                    CG = CGA + CGInc*MO.Obj_02AnimCurrentStep
                    # The difference between the current center of gravity and the object's base
                    gap2 = MO.Objects[n].Shape.CenterOfGravity - MO.Objects[n].Placement.Base
                    # The base of object will be the difference between the center of gravity and the gap2
                    vector = CG - gap2
                    MO.Objects[n].Placement.Base = vector

    # New - Refreshes each step of objects animation
    if OBJ_REFRESH == True:
        FreeCAD.ActiveDocument.recompute()

# ======================================================================================

# 3. Commands

if FreeCAD.GuiUp:
    FreeCAD.Gui.addCommand('CreateMovieObjects', CreateMovieObjects())
    FreeCAD.Gui.addCommand('EnableMovieObjects', EnableMovieObjects())
    FreeCAD.Gui.addCommand('SetMovieObjectsAxis', SetMovieObjectsAxis())
    FreeCAD.Gui.addCommand('ExcludeMovieObjects', ExcludeMovieObjects())

# ======================================================================================
