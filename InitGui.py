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
import RecordPlayVideo as rpv

translate = FreeCAD.Qt.translate

FreeCADGui.addLanguagePath(rpv.LanguagePath)

class Movie (Workbench):
    """The Movie Workbench."""

    from PySide.QtCore import QT_TRANSLATE_NOOP

    MenuText = "Movie"
    ToolTip = QT_TRANSLATE_NOOP("Movie", "Workbench to create and visualize videos of animations in FreeCAD")
    Icon = """
/* XPM */
static char * Movie_xpm[] = {
/* columns rows colors chars-per-pixel */
"15 13 45 1 ",
"  c black",
". c #060606",
"X c #0E0E0E",
"o c #111111",
"O c #131313",
"+ c gray8",
"@ c #151515",
"# c #191919",
"$ c gray10",
"% c gray11",
"& c #1D1D1D",
"* c gray12",
"= c #222222",
"- c #272727",
"; c #282828",
": c gray16",
"> c #2D2D2D",
", c gray18",
"< c #2F2F2F",
"1 c gray19",
"2 c #313131",
"3 c #353535",
"4 c gray21",
"5 c gray22",
"6 c #3C3C3C",
"7 c gray24",
"8 c #3F3F3F",
"9 c #414141",
"0 c gray26",
"q c gray27",
"w c #464646",
"e c gray28",
"r c #484848",
"t c #494949",
"y c gray29",
"u c #4C4C4C",
"i c gray31",
"p c #505050",
"a c #515151",
"s c #555555",
"d c #656565",
"f c #868686",
"g c gray59",
"h c gray64",
"j c white",
/* pixels */
"o@26@#s=@1y+@p:",
"X id @h< uf .g4",
"O>70>1t3>6w>,r$",
"ujjjjjjjjjjjjjp",
"ujjjjjjjjjjjjjp",
"ujjjjjjjjjjjjjp",
"ujjjjjjjjjjjjjp",
"ujjjjjjjjjjjjjp",
"ujjjjjjjjjjjjjp",
"ujjjjjjjjjjjjjp",
"o;58;:t<;5q--e$",
"X id @h< uf .g4",
"+&49&*s;&3u%%a;"
};
"""
                
    def Initialize(self):
        """This function is executed when the workbench is first activated.
        It is executed once in a FreeCAD session followed by the Activated function.
        """
        import RecordPlayVideo # import here all the needed files that create your FreeCAD commands
        import MovieCamera
 
        self.list1 = ['CreateClapperboard',
                      'StartRecord3DView', 
                      'StartRecordRender',
                      'StopRecordCamera',
                      'CreateVideo',
                      'PlayVideo'] # a list of command names created in the line above
        self.appendToolbar("Movietools", self.list1) # creates a new toolbar with your commands
        self.appendMenu("Movie", self.list1) # creates a new menu
        self.list2 = ['MovieCamera',
                      'CreateMovieCamera',
                      'EnableMovieCamera',
                      'SetMovieCameraPosA',
                      'SetMovieCameraPosB',
                      'IniMovieAnimation', 
                      'PrevMovieAnimation',
                      'PauseMovieAnimation',
                      'PlayMovieAnimation',
                      'PostMovieAnimation',
                      'EndMovieAnimation'] # a list of command names created in the line above
        self.appendToolbar("MovieCameratools", self.list2) # creates a new toolbar with your commands        
        self.appendMenu("Movie", self.list2) # creates a new menu

    def Activated(self):
        """This function is executed whenever the workbench is activated"""
        from PySide.QtCore import QT_TRANSLATE_NOOP
        FreeCAD.Console.PrintMessage(QT_TRANSLATE_NOOP("Movie","Movie workbench loaded") + "\n")
        return

    def Deactivated(self):
        """This function is executed whenever the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("Movie tools", self.list) # add commands to the context menu
        
    def GetClassName(self): 
        # This function is mandatory if this is a full Python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"
            
Gui.addWorkbench(Movie())

#https://wiki.freecadweb.org/Workbench_creation
#https://wiki.freecad.org/Translating_an_external_workbench
