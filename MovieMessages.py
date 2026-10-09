'''Frequently used messages for the Movie workbench.'''

# ***************************************************************************
# *   Copyright (c) 2026 Francisco Rosa                                     *
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

"""Collects the most frequently used messages for the Movie Workbench."""

import os
import FreeCAD
import FreeCADGui as Gui

translate = FreeCAD.Qt.translate

_dir = os.path.dirname(__file__)
IconPath = os.path.join(_dir, 'icons')
LanguagePath = os.path.join(_dir, 'translations')
Gui.addLanguagePath(LanguagePath)

#==================================================================

VIEW_00 = translate('MovieAnimation', '3D view')
VIEW_01 = translate('MovieAnimation', 'Render')

TIP_CONNECTION = translate('MovieAnimation',
                           'Connection is enable, you must select \n'
                           'one connection in “Cam_07Connection“!')

MESSAGE = translate('MovieClapperboard',
                    'Note: \n'
                    'This version of FreeCAD seems unable to import cv2!\n'
                    'To create or play back a video, try a different version, like 1.0, \n'
                    'or use the images generated here in an external recording program.')  + '\n'
TIP_ANIM_INIT = translate('App::Property',
                        'Initial step of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the step and/or frame which this \n'
                        'section of the animation and/or recording \n'
                        'will begin.')
TIP_ANIM_END = translate('App::Property',
                        'End step of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the step which this section of \n'
                        'the animation will finish.')
TIP_FRAME_NAME = translate('App::Property',
                        'Name of frame of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the main name of frames. Write a \n'
                        'short name, as this will be inserted in \n'
                        'the nomenclature of each one created.')
TIP_FRAME_WIDTH = translate('App::Property',
                        'Width of frames of the Clapperboard animation.\n'
                        '\n'
                        'Configure the width in pixels of the frames.')
TIP_FRAME_HEIGHT = translate('App::Property',
                        'Height of frames of the Clapperboard animation.\n'
                        '\n'
                        'Configure the height in pixels of the frames.')
TIP_FRAME_OUTPUT = translate('App::Property',
                        'Output path of the Clapperboard animation frames.\n'
                        '\n'
                        'Confirm the folder where the animation frames \n'
                        'will be saved.\n'
                        '\n'
                        'If you wish to preserve the generated images \n'
                        '(in the case of rendered ones, for example), \n'
                        'specify a folder other than the temporary folder.')
TIP_FRAME_TYPE = translate('App::Property',
                        'Type of frame of the Clapperboard animation.\n'
                        '\n'
                        'Select the type of image to be generated: from \n'
                        'the FreeCAD 3D view or rendered. For the latter \n'
                        'option, you must specify a project already prepared \n'
                        'using the Render Workbench.')
TIP_FRAME_RENDER = translate('App::Property',
                        'To use images rendered by the Render Workbench, '
                        'you must specify an existing Render Project!')
TIP_RENDER_PROJECT = translate('MovieClapperboard',
                        'Select a Render Project')
TIP_VIDEO_NAME = translate('App::Property',
                        'Name of the video of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the main name for the created videos. \n'
                        'If you prefer, chose to add manually “3D view“ \n'
                        'text or “Render” one, according to the origin \n'
                        'of the frames.')
TIP_VIDEO_NUMBER = translate('App::Property',
                        'Number of the video of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the initial number of the videos. This will \n'
                        'be inserted in the nomenclature of each one created.')
TIP_VIDEO_OUTPUT = translate('App::Property',
                        'Output path for the video of the Clapperboard \n'
                        'animation.\n'
                        '\n'
                        'Set path to folder to save created videos by \n'
                        'clicking on the button with the three dots \n'
                        'on the right.')
TIP_VIDEO_FPS = translate('App::Property',
                        'Fps of the video of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the frames per second (fps) of the video \n'
                        'that will be created.')
TIP_VIDEO_PLAY = translate('App::Property',
                        'Read-only. \n'
                        '\n'
                        'Indicates whether the animation video will play \n'
                        'automatically after being generated.')