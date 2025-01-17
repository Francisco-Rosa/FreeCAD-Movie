''' Movie workbench, Movie Clapperboard to record and play animation and videos in FreeCAD '''

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

import os
import FreeCAD
import FreeCADGui as Gui
import shutil
import time
from PySide.QtGui import QFileDialog
from PySide.QtCore import QT_TRANSLATE_NOOP
import MovieAnimation as ma

translate = FreeCAD.Qt.translate

_dir = os.path.dirname(__file__)
IconPath = os.path.join(_dir, 'icons')
LanguagePath = os.path.join(_dir, 'translations')
#LanguagePath = os.path.dirname(__file__) + '/translations'
Gui.addLanguagePath(LanguagePath)

CL = None

# ======================================================================================
# 1. Classes

# 1.1. Clapperboard - Movie Record toolbar

class Clapperboard:
    def __init__(self, obj):

        # Animation config
        obj.addProperty('App::PropertyInteger', 'Clap_01AnimIniStep', 'Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                'Initial step of the Clapperboard animation. '
                                                'Indicate the step and/or frame which this section of the animation and/or recording will begin.'
                                                )).Clap_01AnimIniStep = 0
        obj.addProperty('App::PropertyInteger', 'Clap_02AnimCurrentStep', 'Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                'Current step of the Clapperboard animation. It is only indicative.'
                                                )).Clap_02AnimCurrentStep = 0
        obj.addProperty('App::PropertyInteger', 'Clap_03AnimEndStep', 'Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                'End step of the Clapperboard animation. '
                                                'Indicate the step which this section of the animation will finish.'
                                                )).Clap_03AnimEndStep = 100
        obj.addProperty('App::PropertyInteger', 'Clap_04AnimTotalSteps', 'Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                'Total steps of the Clapperboard animation. '
                                                'Indicates the number of steps through which the animation and/or '
                                                'the recording will be performed in this section. It is only indicative.'
                                                )).Clap_04AnimTotalSteps = 100
        obj.addProperty('App::PropertyInteger', 'Clap_05AnimFps', 'Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                'Animation fps of the Clapperboard. '
                                                'Indicate the fps through which the section of the animation will be '
                                                'performed. It is a simulation and will depend on the '
                                                'computer performance.')).Clap_05AnimFps = 30
        obj.addProperty('App::PropertyString', 'Clap_06AnimTime', 'Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                 'Animation time of the Clapperboard. '
                                                 'Time in hours, minutes and seconds. '
                                                 'It is only indicative.'
                                                 )).Clap_06AnimTime = time.strftime("%H:%M:%S", time.gmtime(3.33))

        # Clapperboard config
        obj.addProperty('App::PropertyString', 'Clap_01Name', 'Clapperboard config', QT_TRANSLATE_NOOP('App::Property', 
                                             'Name for this Clapperboard. '
                                             'Indicate the chosen Clapperboard through which the animation and '
                                             'the recording will be performed. Write a short name, as this will be inserted in the '
                                             'nomenclature of each frame created.')).Clap_01Name = 'Clap_00'
        obj.addProperty('App::PropertyString', 'Clap_02Take', 'Clapperboard config', QT_TRANSLATE_NOOP('App::Property', 
                                             'Take of the Clapperboard animation. '
                                             'Indicate the take of each recording made. Write a short name, '
                                             'as this will be inserted in the nomenclature of each frame '
                                             'created.')).Clap_02Take = 'Take_01'
        obj.addProperty('App::PropertyLinkList', 'Clap_03AnimationSelection', 'Clapperboard config', QT_TRANSLATE_NOOP('App::Property', 
                                              'Selection of the Clapperboard animation. '
                                              'Select the MovieCameras and/or the MovieObjects to animate with this Clapperboard.'
                                               )).Clap_03AnimationSelection = None
        obj.addProperty('App::PropertyBool', 'Clap_04OnRec', 'Clapperboard config', QT_TRANSLATE_NOOP('App::Property', 
                                             'Recording Clapperboard animation on or off. '
                                             'It is activated by the “R1“ or “R2“ buttons and deactivated by the Stop Recording one.'
                                             )).Clap_04OnRec = False

        # Frames config
        obj.addProperty('App::PropertyString', 'Frame_01Name', 'Frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Name of frame of the Clapperboard animation. '
                                             'Indicate the main name of these frames. Write a short name, '
                                             'as this will be inserted in the nomenclature of each one '
                                             'created.')).Frame_01Name = str(FreeCAD.ActiveDocument.Label)
        obj.addProperty('App::PropertyInteger', 'Frame_02Width', 'Frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Width of frames of the Clapperboard animation. '
                                             'Only valid for “R1“ frames. '
                                             'Configure the width in pixels of the created frames.')).Frame_02Width = 800
        obj.addProperty('App::PropertyInteger', 'Frame_03Height', 'Frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Height of frames of the Clapperboard animation. '
                                             'Only valid for “R1“ frames.'
                                             'Configure the heigth in pixels of the created frames.')).Frame_03Height = 600
        obj.addProperty('App::PropertyPath', 'Frame_04OutputPath', 'Frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Output path of the Clapperboard animation. '
                                             'Indicate the output folder to save “R1“ or “R2“ frames.')).Frame_04OutputPath = ""
        obj.addProperty('App::PropertyEnumeration', 'Frame_05Type', 'Frames config', QT_TRANSLATE_NOOP('App::Property', 
                                              'Type of frame of the Clapperboard animation. Indicates the type of frame '
                                              'to be saved. It is controlled by the “R1“ or “R2“ buttons.'
                                               )).Frame_05Type = ('R1-3DView', 'R2-Render')
        obj.addProperty('App::PropertyBool', 'Frame_06R1OnRec', 'Frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             '“R1“ recording of the Clapperboard animation on or off. '
                                             'Indicates whether the chosen camera is recording the FreeCAD 3D views or not.'
                                             ' Control this by the “R1“ and Stop Recording buttons.')).Frame_06R1OnRec = False
        obj.addProperty('App::PropertyBool', 'Frame_07R2OnRec', 'Frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             '“R2“ recording of the Clapperboard animation on or off. '
                                             'It indicates whether the chosen camera is recording the renders or not.'
                                             ' Control this by the “R2“ and Stop Recording buttons.')).Frame_07R2OnRec = False 
        obj.addProperty('App::PropertyString', 'Frame_08R2RenderProject', 'Frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Render Project of the Clapperboard animation. '
                                             'Indicate the internal name (not its label) of one of the previously created '
                                             'render projects.')).Frame_08R2RenderProject = "Project"

        # Video group config
        obj.addProperty('App::PropertyString', 'Video_01Name', 'Video config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Name of the video of the Clapperboard animation. Indicate the main name for the created videos. '
                                             'If you prefer, chose to add manually “3DViews“ text or “Renders“ one, according to the origin of the '
                                             'frames.')).Video_01Name = str(FreeCAD.ActiveDocument.Label)
        obj.addProperty('App::PropertyInteger', 'Video_02Number', 'Video config',  QT_TRANSLATE_NOOP('App::Property',
                                              'Number of the video of the Clapperboard animation. '
                                              'Indicate the initial number of the videos (zero for the first one). '
                                             'This will be inserted in the nomenclature of each one created.')).Video_02Number = 0
        obj.addProperty('App::PropertyPath', 'Video_03InputFrames', 'Video config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Input frames for the video of the Clapperboard animation. '
                                             'Confirm the path to the folder containing the frames for creating a video '
                                             'by clicking on the Create video button or on the three dots on the right.'
                                             )).Video_03InputFrames = ""
        obj.addProperty('App::PropertyPath', 'Video_04OutputPath', 'Video config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Output path for the video of the Clapperboard animation. '
                                             'Set path to folder to save created videos by clicking on the button with '
                                             'the three dots on the right.')).Video_04OutputPath = ""
        obj.addProperty('App::PropertyInteger', 'Video_05Fps','Video config', QT_TRANSLATE_NOOP('App::Property',
                                             'Fps of the video of the Clapperboard animation. '
                                             'Indicate the frames per second (fps) of the video that will be created.'
                                             )).Video_05Fps = 24

        obj.Proxy = self

class ClapperboardViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/ClapperboardIcon.svg'

class CreateClapperboard:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/CreateClapperboardIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('CreateClapperboard', 'Clapperboard'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateClapperboard',
                                             'Create a Clapperboard to play and record animations. '
                                             'Once created and before enabling it, complete or modify '
                                             'each of its properties.')}

    def Activated(self):
        ActivatedClapperboard(self)

def ActivatedClapperboard(self):

    default_label = translate('Movie', 'Clapperboard')
    folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'Clapperboard')
    Clapperboard(folder)
    ClapperboardViewProvider(folder.ViewObject)
    folder.Label = default_label

class EnableMovieClapperboard:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/EnableMovieClapperboardIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('EnableMovieClapperboard', 'Enables a Clapperboard'),
                'ToolTip': QT_TRANSLATE_NOOP('EnableMovieClapperboard', 
                                             'Enable a Clapperboard. First, select the Clapperboard that you want to configure, '
                                             'then click this button to activate it.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        global CL
        CL = ma.enableMovieClapperboard()

class StartRecord3DView:

    def QT_TRANSLATE_NOOP(Render, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/StartRecord3DViewIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('StartRecord3DView', '“R1“ - Record 3DViews'),
                'ToolTip': QT_TRANSLATE_NOOP('StartRecord3DView', 
                                             'Triggers the recording of frames according to '
                                             'the “Frames config“ of the properties window of the Clapperboard. '
                                             'After clicking on it, confirm the folder to save the frames '
                                             'and play the animation.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not CL.Clap_04OnRec:
                return True
        else:
            return False

    def Activated(self):
        startRecord3DView()

class StartRecordRender:

    def QT_TRANSLATE_NOOP(Render, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/StartRecordRenderIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('StartRecordRender', '“R2“ - Record renders'),
                'ToolTip': QT_TRANSLATE_NOOP('StartRecordRender', 
                                             'Triggers the recording of frames according to '
                                             'the “Frames config“ of the properties window of the Clapperboard. '
                                             'After clicking on it, confirm the folder to salve the frames '
                                             'and play the animation.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not CL.Clap_04OnRec:
                return True
        else:
            return False

    def Activated(self):
        startRecordRender()

class StopRecordCamera:

    def QT_TRANSLATE_NOOP(Render, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/StopRecordCameraIcon.svg',
                'Accel': 'Ctrl+k',
                'MenuText': QT_TRANSLATE_NOOP('StopRecordCamera', 'Stop recording'),
                'ToolTip': QT_TRANSLATE_NOOP('StopRecordCamera','Stop the Clapperboard recording.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if CL.Clap_04OnRec:
                return True
        else:
            return False

    def Activated(self):
        stopRecordCamera(Clap = CL)

class CreateVideo:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/CreateVideoIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('CreateVideo', 'Create video'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateVideo', 
                                             'Create a mp4 video of an animation according to the '
                                             'settings previously made in the Clapperboard. After '
                                             'clicking, confirm the folder to save the video.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not CL.Clap_04OnRec:
                return True
        else:
            return False

    def Activated(self):
        createVideo()

class PlayVideo:

    def QT_TRANSLATE_NOOP(Render, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PlayVideoIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PlayVideo', 'Play video'),
                'ToolTip': QT_TRANSLATE_NOOP('PlayVideo', 
                                             'Play a video file indicated in the dialog window.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not CL.Clap_04OnRec:
                return True
        else:
            return False

    def Activated(self):
        playVideo()

# ======================================================================================
# 2. Command functions

# 2.1. Frames recording commands

def startRecord3DView():
    global CL
    CL.Clap_04OnRec = True
    CL.Frame_05Type = 'R1-3DView'
    CL.Frame_06R1OnRec = True
    WindowTitle = translate('Movie', 'Select or confirm the folder to save the “R1“ frames')
    OpenDir = CL.Frame_04OutputPath
    CL.Frame_04OutputPath = QFileDialog.getExistingDirectory(Gui.getMainWindow(), WindowTitle, OpenDir)

def startRecordRender():
    global CL
    import Render
    global START_RENDER_FRAME
    START_RENDER_FRAME = CL.Clap_02AnimCurrentStep
    CL.Frame_05Type = 'R2-Render'
    CL.Clap_04OnRec = True
    CL.Frame_07R2OnRec = True
    WindowTitle = translate('Movie', 'Select or confirm the folder to save the “R2“ frames')
    OpenDir = CL.Frame_04OutputPath
    CL.Frame_04OutputPath = QFileDialog.getExistingDirectory(Gui.getMainWindow(), WindowTitle, OpenDir)

def stopRecordCamera(Clap = None):
    global CL
    CL = Clap
    CL.Clap_04OnRec = False
    CL.Frame_06R1OnRec = False
    CL.Frame_07R2OnRec = False

def runRecordCamera(Back = False):
    camNum = str(f'{CL.Clap_01Name:0>2}')
    takeNum = str(f'{CL.Clap_02Take:0>2}')

    if CL.Frame_06R1OnRec == True:
        if Back == False:
            frameNum = str(f'{CL.Clap_02AnimCurrentStep:0>4}')
        else:
            frameNum = str(f'{(CL.Clap_04AnimTotalSteps - CL.Clap_02AnimCurrentStep):0>4}')
        #frameFinalName = f'{CL.Frame_01Name}_{camNum}_{takeNum}_{CL.Frame_05Type}_{frameNum}.png'
        frameFinalName = f'{CL.Frame_01Name}_{camNum}_{takeNum}_{CL.Frame_05Type}_{frameNum}.jpg'
        pathAndName = CL.Frame_04OutputPath +'/' + frameFinalName
        Gui.activeDocument().activeView().saveImage(pathAndName,CL.Frame_02Width,CL.Frame_03Height,'Current')
        FreeCAD.Console.PrintMessage(translate('Movie', 'Frame 3DView {} has been completed.').format(frameNum) + '\n')

    if CL.Frame_07R2OnRec == True :
        if Back == False:
            frameNum = str(f'{CL.Clap_02AnimCurrentStep:0>4}')
        else:
            frameNum = str(f'{(CL.Clap_04AnimTotalSteps - CL.Clap_02AnimCurrentStep):0>4}')
        frameFinalName = f'{CL.Frame_01Name}_{camNum}_{takeNum}_{CL.Frame_05Type}_{frameNum}.png'
        project =  FreeCAD.getDocument(FreeCAD.ActiveDocument.Label).getObject(CL.Frame_08R2RenderProject)
        if CL.Clap_02AnimCurrentStep == START_RENDER_FRAME:
            output_file=project.Proxy.render(skip_meshing=False, wait_for_completion=True)
        else:
            output_file=project.Proxy.render(skip_meshing=True, wait_for_completion=True)
        shutil.move(output_file, f"" + f'{CL.Frame_04OutputPath}/{frameFinalName}')
        # Close render window
        if project.OpenAfterRender:
            Gui.runCommand('Std_CloseActiveWindow',0)
        FreeCAD.Console.PrintMessage(translate('Movie', 'Frame render {} has been completed.').format(frameNum) + '\n')

# ======================================================================================
# 2.2. Create and play video commands

def createVideo():
    global CL
    import cv2

    # Confirmation of the input frames folder to create video
    WindowTitle1 = translate('Movie', 'Select or confirm the input frames folder to create video')
    OpenDir = CL.Frame_04OutputPath
    CL.Video_03InputFrames = QFileDialog.getExistingDirectory(Gui.getMainWindow(), WindowTitle1, OpenDir)

    pathFrames = CL.Video_03InputFrames +'/'
    outVideoPath = CL.Video_04OutputPath + '/'
    CL.Video_02Number += 1
    videoNum = str(f'{CL.Video_02Number:0>2}')
    outVideoName = str(f'{CL.Video_01Name}_{CL.Clap_01Name}_{CL.Clap_02Take}_{CL.Frame_05Type}_{videoNum}.mp4')
    outVideoFullPath = outVideoPath+outVideoName

    cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    inFrames = sorted(os.listdir(pathFrames))

    frames = []

    for i in inFrames:
        i = pathFrames+i
        frames.append(i)

    frame1 = cv2.imread(frames[0])
    size1 = list(frame1.shape)
    del size1[2]
    Heightframe1, Widthframe1 = size1

    fps = CL.Video_05Fps
    # Output video name, fourcc, fps, size (heigth, width)
    video = cv2.VideoWriter(outVideoFullPath, cv2_fourcc, fps, (Widthframe1, Heightframe1))

    for i in range(len(frames)):
        video.write(cv2.imread(frames[i]))
        FreeCAD.Console.PrintMessage(translate('Movie', 'frame {} of {}.').format(i+1, len(frames)) + '\n')

    video.release()
    FreeCAD.Console.PrintMessage(translate('Movie', 'Outputed video to {}').format(outVideoPath)+'\n')

def playVideo():
    import cv2
    import time

    MovieFileFilter = '; All files (*.*)'
    WindowTitle = translate('Movie', 'Select file to play')
    OpenDir = CL.Video_04OutputPath + '/'
    PathAndFile = QFileDialog.getOpenFileName(Gui.getMainWindow(), WindowTitle, OpenDir, MovieFileFilter)

    Video_PathAndFile = PathAndFile[0]

    cap = cv2.VideoCapture(Video_PathAndFile)

    fps2 = int(cap.get(cv2.CAP_PROP_FPS))

    if cap.isOpened() == False:
        FreeCAD.Console.PrintMessage(translate('Movie','Error: video file not found!'))
        return

    else:
        message2 = ('Movie preview at {} fps, press q to stop the video').format(fps2)
        #message2 = (translate('Movie', 'Movie at {} fps, press q to stop the video').format(fps2))

    while cap.isOpened():
        sucess, frame = cap.read()
        if sucess == True:
            time.sleep(1/fps2)
            cv2.imshow(message2, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    #cv2.destroyAllWindows()

# ======================================================================================
# 3. Commands

if FreeCAD.GuiUp:

    FreeCAD.Gui.addCommand('CreateClapperboard', CreateClapperboard())
    FreeCAD.Gui.addCommand('EnableMovieClapperboard', EnableMovieClapperboard())
    FreeCAD.Gui.addCommand('StartRecord3DView', StartRecord3DView())
    FreeCAD.Gui.addCommand('StartRecordRender', StartRecordRender())
    FreeCAD.Gui.addCommand('StopRecordCamera', StopRecordCamera())
    FreeCAD.Gui.addCommand('CreateVideo', CreateVideo())
    FreeCAD.Gui.addCommand('PlayVideo', PlayVideo())

# ======================================================================================

#https://wiki.freecad.org/Command
#https://wiki.freecad.org/Translating_an_external_workbench
