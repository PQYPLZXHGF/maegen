# -*- encoding: UTF-8 -*-

#    Maegen is a genealogical application for N900. Use it on the go
#    to store genealogical data including individuals and relational
#    informations. Maegen can be used to browse collected data on the
#    device but the main goal is its capabilitie to export the dtabase
#    in a GEDCOM file which can be imported into any desktop genealocial
#    application.
#
#    Copyright (C) 2011  Thierry Bressure
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>

'''
Created on Nov 27, 2011

@author: maemo
'''
import logging

import gtk
import gobject
from gtk import gdk


from maegen.common import version

version.getInstance().submitRevision("$Revision$")

class GenTree(gtk.Widget):
    '''
    This widget display a genealogical tree given a root individual
    '''
    def __init__(self, zcore, individual, show_spouse=False):
        gtk.Widget.__init__(self)
        self.root = individual
        self.zcore = zcore
        self.show_spouse=show_spouse
        self.WIDTH_FOR_INDI = 150
        self.HORIZONTAL_SPACE=50
        self.HEIGHT_FOR_INDI = 70
        self.VERTICAL_SPACE = 100
        
    def do_realize(self):
        """Called when the widget should create all of its 
        windowing resources.  We will create our gtk.gdk.Window
        and load our star pixmap."""
        
        # First set an internal flag showing that we're realized
        self.set_flags(self.flags() | gtk.REALIZED)
        
        # Create a new gdk.Window which we can draw on.
        # Also say that we want to receive exposure events 
        # and button click and button press events
            
        self.window = gtk.gdk.Window(
            self.get_parent_window(),
            width=self.allocation.width,
            height=self.allocation.height,
            window_type=gdk.WINDOW_CHILD,
            wclass=gdk.INPUT_OUTPUT,
            event_mask=self.get_events() | gtk.gdk.EXPOSURE_MASK
                | gtk.gdk.BUTTON_PRESS_MASK)
                
        # Associate the gdk.Window with ourselves, Gtk+ needs a reference
        # between the widget and the gdk window
        self.window.set_user_data(self)
        
        # Attach the style to the gdk.Window, a style contains colors and
        # GC contextes used for drawing
        self.style.attach(self.window)
        
        # The default color of the background should be what
        # the style (theme engine) tells us.
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)
        
            
        # self.style is a gtk.Style object, self.style.fg_gc is
        # an array or graphic contexts used for drawing the forground
        # colours    
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        self.connect("expose-event", self.area_expose_cb)    
        
        
    def do_unrealize(self):
        # The do_unrealized method is responsible for freeing the GDK resources
        # De-associate the window we created in do_realize with ourselves
        self.window.destroy()
        
    def do_size_request(self, requisition):
        """From Widget.py: The do_size_request method Gtk+ is calling
         on a widget to ask it the widget how large it wishes to be. 
         It's not guaranteed that gtk+ will actually give this size 
         to the widget.  So we will send gtk+ the size needed for
         the maximum amount of stars"""
        
        
        real_width = self.compute_width()
        self.drawing_area_width = max([800, real_width])
        real_height = self.compute_height() 
        self.drawing_area_height = max([400,real_height])          
        self.pangolayout_name = self.create_pango_layout("")
        self.pangolayout_life = self.create_pango_layout("")
        requisition.height = self.drawing_area_height + 1
        requisition.width = self.drawing_area_width + 1
    
    
    def do_size_allocate(self, allocation):
        """The do_size_allocate is called by when the actual 
        size is known and the widget is told how much space 
        could actually be allocated Save the allocated space
        self.allocation = allocation. The following code is
        identical to the widget.py example"""
    
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*allocation)
        
        
    def area_expose_cb(self, area, event):
        self.draw_tree(self.root, 0, self.drawing_area_width, 0)
        
    def do_expose_event(self, event):
        """This is where the widget must draw itself."""                
        self.area_expose_cb(self.window, event)
        

    def draw_individual(self, indi, x, y):        
        '''
        Parameter:
            - indi: the individual
            - x,y : the center top of the individual node
        '''
        top_left = (x-self.WIDTH_FOR_INDI / 2,y)      
        #self.drawing_area.window.draw_rectangle(self.gc, False, top_left[0], top_left[1], self.WIDTH_FOR_INDI, self.HEIGHT_FOR_INDI)
        # Name
        self.pangolayout_name.set_text(str(indi))
        self.window.draw_layout(self.gc, top_left[0] + 1  , top_left[1] + 1 , self.pangolayout_name)        
        # gender picture if available
        pixbuf = get_gender_pixbuf(indi)
        if pixbuf :
            pixbuf.render_to_drawable(self.window, self.gc, 0,0,top_left[0],top_left[1] + 1 + self.HEIGHT_FOR_INDI / 2,-1,-1)    
            IMAGE_WIDTH = 13
            IMAGE_HEIGTH = 13
                                
        # date life
        life_str = get_life_date_str(indi)
        self.pangolayout_life.set_text(life_str)
        attrs = pango.AttrList()
        attrs.insert(pango.AttrScale(pango.SCALE_X_SMALL,0,len(life_str)))
        self.pangolayout_life.set_attributes(attrs)
        self.window.draw_layout(self.gc, x , top_left[1] + 1 + self.HEIGHT_FOR_INDI / 2 , self.pangolayout_life)
                 
    
    def size_for_individual(self, indi):
        '''
        Compute the width of the tree with the given individual as root
        '''
        logging.debug("compute size required by " + str(indi))
        n = self.zcore.children_count(indi)
        if n == 0:
            logging.debug("No child")
            resu = self.WIDTH_FOR_INDI
        else:
            logging.debug("has child, include children size")
            resu = 0
            for child in self.zcore.retrieve_children(indi):
                logging.debug("child " + str(child) + "...")
                resu += self.size_for_individual(child)
            resu += (n - 1) * self.HORIZONTAL_SPACE            
            logging.debug("adjusted size become " + str(resu))                            
        logging.debug("size required by " + str(indi) + " is " + str(resu))
        return resu
    
    def draw_tree(self, individual, left_corner_x,right_corner_x, top_y ):
        '''
        Draw the individual tree inside the given windows on the drawing area
        Return the x position of the individual node
        '''
        # is there any child ?
        children = self.zcore.retrieve_children(individual)
        if len(children) == 0:
            # draw individual in given window, justify left
            resu = left_corner_x + self.WIDTH_FOR_INDI / 2
            self.draw_individual(individual, resu, top_y)
        else:
            row_left_x = None
            row_right_x = None
            child_left_corner_x = left_corner_x
            top_y_for_child = top_y + self.HEIGHT_FOR_INDI + self.VERTICAL_SPACE
            y_for_horiz_row = top_y_for_child - self.VERTICAL_SPACE / 2            
            for child in children:
                size_for_child = self.size_for_individual(child)
                child_right_corner_x = child_left_corner_x + size_for_child            
                x = self.draw_tree(child, child_left_corner_x, child_right_corner_x, top_y_for_child)      
                # draw the small vertical link
                self.window.draw_line(self.gc, x,top_y_for_child,x, y_for_horiz_row)         
                if row_left_x is None:
                    row_left_x = x
                    row_right_x = x
                else:
                    row_right_x = x
                child_left_corner_x += size_for_child + self.HORIZONTAL_SPACE
            # draw horizontal row
            self.window.draw_line(self.gc,row_left_x,y_for_horiz_row, row_right_x,y_for_horiz_row)
            #compute the root abscisse
            resu = ( row_left_x + row_right_x ) / 2
            # draw the small vertical link
            self.window.draw_line(self.gc,resu,y_for_horiz_row, resu, y_for_horiz_row - self.VERTICAL_SPACE / 2)            
            # draw the root node            
            self.draw_individual(individual, resu, top_y)
        return resu        
        
    def compute_width(self):    
        return self.size_for_individual(self.root)

    def compute_height(self):

        def depth_for_individual(indi):
            if self.zcore.children_count(indi) == 0:
                return 1
            else:                
                depth_of_children = map(depth_for_individual,self.zcore.retrieve_children(indi))
                depth_from_indi = map(lambda child_depth: child_depth+1, depth_of_children)
                return max(depth_from_indi)
        
        depth = depth_for_individual(self.root)
        return  depth *  self.HEIGHT_FOR_INDI + ( depth - 1) * self.VERTICAL_SPACE

gobject.type_register(GenTree)