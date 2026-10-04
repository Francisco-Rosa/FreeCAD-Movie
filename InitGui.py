"""FreeCAD init script of Movie Workbench"""

# ***************************************************************************
# *   Copyright (c) 2022 Francisco Rosa                                     *
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

"""Gui initialization module for Movie Workbench."""

import FreeCAD
import FreeCADGui as Gui
import MovieClapperboard as cl

FreeCADGui.addLanguagePath(cl.LanguagePath)
FreeCADGui.updateLocale()

class Movie (Workbench):
    """The Movie Workbench."""

    translate = FreeCAD.Qt.translate

    MenuText = translate("InitGui", "Movie")
    ToolTip = translate("InitGui", "Workbench to create and visualize animations and videos in FreeCAD")
    from MovieClapperboard import IconPath
    Icon = os.path.join(IconPath, "MovieWBIcon.svg")

    def Initialize(self):
        """This function is executed when the workbench is first activated.
        It is executed once in a FreeCAD session followed by the Activated function.
        """
        # import here all the needed files that create your FreeCAD commands
        import MovieClapperboard
        import MovieCamera
        import MovieObject
        import MovieAnimation
        translate = FreeCAD.Qt.translate

        self.list1 = ['CreateMovieCamera',
                      'EnableMovieCamera',
                      'SetMoviePosA',
                      'SetMoviePosB',
                      'CreateMovieObjects',
                      'EnableMovieObjects',
                      'SetMovieObjectsAxis',
                      'ExcludeMovieObjects',] # a list of command names created in the line above

        default_title1 = translate("InitGui", "Cameras and objects tools")
        default_title2 = translate("InitGui", "Cameras and Objects")
        self.appendToolbar(default_title1, self.list1) # creates the Movie Cameras and Objects toolbar with your commands
        self.appendMenu(default_title2, self.list1) # creates the Movie Cameras and Objects menu

        self.list2 = ['IniMovieAnimation',
                      'PrevMovieAnimation',
                      'PlayBackwardMovieAnimation',
                      'PauseMovieAnimation',
                      'PlayMovieAnimation',
                      'PostMovieAnimation',
                      'EndMovieAnimation'] # a list of command names created in the line above

        default_title3 = translate("InitGui", "Animation tools")
        default_title4 = translate("InitGui", "Animation")
        self.appendToolbar(default_title3, self.list2) # creates the Movie Animation toolbar with your commands
        self.appendMenu(default_title4, self.list2) # creates the Movie Animation menu

        self.list3 = ['CreateClapperboard',
                      'EnableMovieClapperboard',
                      'StartRecord3DView',
                      'StartRecordRender',
                      'StopRecordCamera',
                      'CreateVideo',
                      'PlayVideo'] # a list of command names created in the line above

        default_title5 = translate("InitGui", "Record and play tools")
        default_title6 = translate("InitGui", "Record and Play")
        self.appendToolbar(default_title5, self.list3) # creates the Movie Record and Play toolbar with your commands
        self.appendMenu(default_title6, self.list3) # creates the Movie Record and Play menu

    def Activated(self):
        """This function is executed whenever the workbench is activated"""

        translate = FreeCAD.Qt.translate

        FreeCAD.Console.PrintMessage(translate("InitGui","Movie Workbench loaded") + "\n")
        return

    def Deactivated(self):
        """This function is executed whenever the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""

        translate = FreeCAD.Qt.translate

        # "recipient" will be either "view" or "tree"
        default_title1 = translate("ContextMenu", "Cameras and Objects")
        default_title2 = translate("ContextMenu", "Animation")
        default_title3 = translate("ContextMenu", "Record and Play")
        self.appendContextMenu(default_title1, self.list1) # add commands to the context menu
        self.appendContextMenu(default_title2, self.list2) # add commands to the context menu
        self.appendContextMenu(default_title3, self.list3) # add commands to the context menu

    def GetClassName(self):
        # This function is mandatory if this is a full Python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"

Gui.addWorkbench(Movie())

#https://wiki.freecadweb.org/Workbench_creation
#https://wiki.freecad.org/Translating_an_external_workbench
