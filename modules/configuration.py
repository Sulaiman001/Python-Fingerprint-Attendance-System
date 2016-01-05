# coding=UTF-8

try:
 	import pygtk
  	pygtk.require("2.4")
except:
  	pass

import threading
import time
from gettext import gettext as _
import gtk
import os
from configobj import ConfigObj

class ConfigurationManager:
    def __init__(self):
        self.__filename = os.path.abspath("config/attendance_system.cfg")
        self.__config_param = {}

    def load_configurations(self):
        try:
            self.__config_param = ConfigObj(self.__filename)
        except:
            self.__config_param = None
   
    def save_configurations(self, configurations):
        config = ConfigObj()
        config.filename =  self.__filename
        config = configurations
        self.__config_param = configurations
        try:        
            config.write()
            return True
        except:
            return False

    def get_configurations(self):
        return self.__config_param

class ConfigSection:
    def __init__(self, parent_window, parent_box, config_manager, dev):
        self.__config_param = config_manager.get_configurations()
        self.__config_manager = config_manager
        self.__parent_window = parent_window
        self.__dev = dev
        self.last_chb_clicked = None

        # Main Boxes        
        configurations_vbox = gtk.VBox(False, 0)
        sections_hbox = gtk.HBox(False,0)
        button_hbox = gtk.HBox(False,0)
        configurations_vbox.pack_start(sections_hbox,True,False,0)
        configurations_vbox.pack_start(button_hbox,True,False,0)
        
        # Option Sections
        left_vbox = gtk.VBox(False,0)
        right_vbox = gtk.VBox(False,0)
        sections_hbox.pack_start(left_vbox, True, True, 0)
        sections_hbox.pack_start(right_vbox, True, True, 0) 
        
        # Attendance Options
        attendance_options_box = gtk.VBox(False,0)
        frame_general_options = gtk.Frame(_("Assist Control Options"))
        frame_general_options.add(attendance_options_box)
        left_vbox.pack_start(frame_general_options, True, False, 0)
        self.__rb_dni = gtk.RadioButton(None, _("Use Card Number"))
        attendance_options_box.pack_start(self.__rb_dni, False, False, 5)                
        if self.__config_param["app"]["attendance_by_dni"] == "True":
            self.__rb_dni.set_active(True)
        else:
            self.__rb_dni.set_active(False)
        self.__rb_user_name = gtk.RadioButton(self.__rb_dni, _("Use Username"))        
        attendance_options_box.pack_start(self.__rb_user_name, False, False, 5)        
        if self.__config_param["app"]["attendance_by_user_name"] == "True":
            self.__rb_user_name.set_active(True)
        else:
            self.__rb_user_name.set_active(False)
        self.__op_chb_events = gtk.CheckButton(_("Support for events"))
        attendance_options_box.pack_start(self.__op_chb_events, False, False, 5)
        if self.__config_param["app"]["events_attendance"] == "True":
            self.__op_chb_events.set_active(True)
        else:
            self.__op_chb_events.set_active(False)

        #Finger Print Options
        fp_options_box = gtk.VBox(False,0)
        frame_fp_options = gtk.Frame(_("Fingerprint Options"))
        frame_fp_options.add(fp_options_box)
        left_vbox.pack_start(frame_fp_options, True, False, 0)
        if self.__dev != None:        
            try:            
                dev_label = gtk.Label(_("Device: ") + str(self.__dev.get_driver().get_full_name()))
            except:
                dev_label = gtk.Label(_("Device: unknown"))
        else:
            dev_label = gtk.Label(_("Device: Not Found"))
        fp_options_box.pack_start(dev_label, True, False, 5)
        self.__op_chb_finger_print = gtk.CheckButton(_("Using Fingerprint"))        
        fp_options_box.pack_start(self.__op_chb_finger_print, False, False, 5)
        if self.__dev != None:        
            if self.__config_param["app"]["attendance_by_finger_print"] == "True":
                self.__op_chb_finger_print.set_active(True)
            else:
                self.__op_chb_finger_print.set_active(False)
        else:
            self.__op_chb_finger_print.set_active(False)
            self.__op_chb_finger_print.set_sensitive(False)
        label = gtk.Label(_("Hand"))
        fp_options_box.pack_start(label,False,False,5)
        self.__r_right_hand = gtk.RadioButton(None, _("Right"))        
        fp_options_box.pack_start(self.__r_right_hand,True,False,0)
        self.__r_left_hand = gtk.RadioButton(self.__r_right_hand, _("Left"))        
        fp_options_box.pack_start(self.__r_left_hand,True,False,0)
        if self.__config_param["finger_print"]["hand"] == "right":
            self.__r_right_hand.set_active(True)
        elif self.__config_param["finger_print"]["hand"] == "left":
            self.__r_left_hand.set_active(True)
        label = gtk.Label(_("Finger"))
        fp_options_box.pack_start(label,False,False,5)
        self.__r_thumb_finger = gtk.RadioButton(None, _("Thumb"))
        fp_options_box.pack_start(self.__r_thumb_finger,True,False,0)
        self.__r_index_finger = gtk.RadioButton(self.__r_thumb_finger, _("Table of Contents"))
        fp_options_box.pack_start(self.__r_index_finger,True,False,0)
        self.__r_middle_finger = gtk.RadioButton(self.__r_thumb_finger, _("Middle"))
        fp_options_box.pack_start(self.__r_middle_finger,True,False,0)
        self.__r_ring_finger = gtk.RadioButton(self.__r_thumb_finger, _("Cancel"))
        fp_options_box.pack_start(self.__r_ring_finger,True,False,0)
        self.__r_little_finger = gtk.RadioButton(self.__r_thumb_finger, _("Littel Finger"))        
        fp_options_box.pack_start(self.__r_little_finger,True,False,0)
        if self.__config_param["finger_print"]["finger"] == "thumb":
            self.__r_thumb_finger.set_active(True)
        elif self.__config_param["finger_print"]["finger"] == "index":
            self.__r_index_finger.set_active(True)
        elif self.__config_param["finger_print"]["finger"] == "middle":
            self.__r_middle_finger.set_active(True)
        elif self.__config_param["finger_print"]["finger"] == "ring":
            self.__r_ring_finger.set_active(True)
        elif self.__config_param["finger_print"]["finger"] == "little":
            self.__r_little_finger.set_active(True)
        self.__op_chb_finger_print.connect('clicked', self.__enable_fp_radiobuttons)
        self.__enable_fp_radiobuttons(self.__op_chb_finger_print)

        # Database Options       
        frame_db_options = gtk.Frame(_("Database Configuration"))
        table_hbox = gtk.HBox(False,0)
        table_db_options = gtk.Table(rows=4, columns=2, homogeneous=True)
        table_hbox.pack_start(table_db_options,False,False,0)
        frame_db_options.add(table_hbox)        
        right_vbox.pack_start(frame_db_options, True, True, 0)
        
        #DB Name        
        label = gtk.Label(_("Name"))
        table_db_options.attach(label,0,1,0,1)
        self.__e_db_name = gtk.Entry()
        self.__e_db_name.set_text(self.__config_param["database"]["name"])
        table_db_options.attach(self.__e_db_name,1,2,0,1)

        #DB User Name
        label = gtk.Label(_("User"))
        table_db_options.attach(label,0,1,1,2)
        self.__e_db_user = gtk.Entry()
        self.__e_db_user.set_text(self.__config_param["database"]["user"])
        table_db_options.attach(self.__e_db_user,1,2,1,2)

        #DB User Name Password
        label = gtk.Label(_("Password"))
        table_db_options.attach(label,0,1,2,3)
        self.__e_db_password = gtk.Entry()
        self.__e_db_password.set_text(self.__config_param["database"]["password"])
        table_db_options.attach(self.__e_db_password,1,2,2,3)

        #DB Host
        label = gtk.Label(_("Host"))
        table_db_options.attach(label,0,1,3,4)
        self.__e_db_host = gtk.Entry()
        self.__e_db_host.set_text(self.__config_param["database"]["host"])
        table_db_options.attach(self.__e_db_host,1,2,3,4)

        # Admin Options
        frame_admin_options = gtk.Frame(_("Configuration Manager"))
        admin_options_vbox = gtk.HBox(False,0)
        frame_admin_options.add(admin_options_vbox)
        right_vbox.pack_start(frame_admin_options, True, True, 0)
        table_admin_options = gtk.Table(rows=4, columns=2, homogeneous=True)
        table_admin_options.set_col_spacings(30)
        admin_options_vbox.pack_start(table_admin_options,False,False,0)
        
        self.__chb_change_admin_password = gtk.CheckButton(_("Change Password"))
        self.__chb_change_admin_password.set_active(False)        
        table_admin_options.attach(self.__chb_change_admin_password,0,2,0,1,gtk.EXPAND)
        
        # Old Password
        label = gtk.Label(_("Current Password"))
        table_admin_options.attach(label,0,1,1,2)
        self.__e_old_password = gtk.Entry()
        self.__e_old_password.set_sensitive(False)
        self.__e_old_password.set_visibility(False)
        table_admin_options.attach(self.__e_old_password,1,2,1,2)

        # New Password
        label = gtk.Label(_("New Password"))
        table_admin_options.attach(label,0,1,2,3)
        self.__e_new_password = gtk.Entry()
        self.__e_new_password.set_sensitive(False)
        self.__e_new_password.set_visibility(False)
        table_admin_options.attach(self.__e_new_password,1,2,2,3)

        # Repeat New Password
        label = gtk.Label(_("Repeat New Password"))
        table_admin_options.attach(label,0,1,3,4)
        self.__e_r_new_password = gtk.Entry()
        self.__e_r_new_password.set_sensitive(False)
        self.__e_r_new_password.set_visibility(False)
        table_admin_options.attach(self.__e_r_new_password,1,2,3,4)
        self.__chb_change_admin_password.connect('clicked', self.__enable_admin_pass_entries_cb)

        #Save Button
        b_save = gtk.Button("Save")
        button_hbox.pack_start(b_save,True,False,0)
        b_save.connect('clicked', self.__save_configurations_cb)

        configurations_vbox.show_all()
        parent_box.pack_start(configurations_vbox,True,True,0)   

    def __show_dialog(self, type_dialog=gtk.MESSAGE_INFO, message=""):
        dialog = gtk.MessageDialog(self.__parent_window, gtk.DIALOG_MODAL, \
                                     type_dialog, gtk.BUTTONS_OK, message)
        dialog.set_title(_("Fingerprint Attendance System"))
        dialog.run()
        dialog.destroy()

    def __enable_admin_pass_entries_cb(self, button):
        if button.get_active():        
            self.__e_old_password.set_sensitive(True)
            self.__e_new_password.set_sensitive(True)
            self.__e_r_new_password.set_sensitive(True)
        else:
            self.__e_old_password.set_sensitive(False)
            self.__e_new_password.set_sensitive(False)
            self.__e_r_new_password.set_sensitive(False)

    def __enable_fp_radiobuttons(self, button):
        if button.get_active():
            self.__r_right_hand.set_sensitive(True)
            self.__r_left_hand.set_sensitive(True)
            self.__r_thumb_finger.set_sensitive(True)
            self.__r_index_finger.set_sensitive(True)
            self.__r_middle_finger.set_sensitive(True)
            self.__r_ring_finger.set_sensitive(True)
            self.__r_little_finger.set_sensitive(True)
        else:
            self.__r_right_hand.set_sensitive(False)
            self.__r_left_hand.set_sensitive(False)
            self.__r_thumb_finger.set_sensitive(False)
            self.__r_index_finger.set_sensitive(False)
            self.__r_middle_finger.set_sensitive(False)
            self.__r_ring_finger.set_sensitive(False)
            self.__r_little_finger.set_sensitive(False)        

    def __save_configurations_cb(self, button):
        # Save database parameters
        changed_db_parameters = False
        if self.__config_param["database"]["name"] != self.__e_db_name.get_text():
            changed_db_parameters = True
        elif  self.__config_param["database"]["user"] != self.__e_db_user.get_text():
            changed_db_parameters = True
        elif self.__config_param["database"]["password"] != self.__e_db_password.get_text():
            changed_db_parameters = True
        elif self.__config_param["database"]["host"] != self.__e_db_host.get_text():
            changed_db_parameters = True
        self.__config_param["database"]["name"] =  self.__e_db_name.get_text()
        self.__config_param["database"]["user"] = self.__e_db_user.get_text()
        self.__config_param["database"]["password"] = self.__e_db_password.get_text()
        self.__config_param["database"]["host"] = self.__e_db_host.get_text()

        # Save New Admin Password
        if self.__chb_change_admin_password.get_active():
            if self.__e_old_password.get_text() == self.__config_param["admin"]["password"]:
                if self.__e_new_password.get_text() == self.__e_r_new_password.get_text():
                    self.__config_param["admin"]["password"] = self.__e_new_password.get_text()
                else:
                    self._show_error_dialog(_("The passwords do not match"))    
            else:
                self._show_error_dialog(_("The administrator password entered is incorrect"))
        
        # Save app options
        if self.__op_chb_finger_print.get_active():
            self.__config_param["app"]["attendance_by_finger_print"] = "True"
        else:
            self.__config_param["app"]["attendance_by_finger_print"] = "False"
        if self.__rb_dni.get_active():
            self.__config_param["app"]["attendance_by_dni"] = "True"
        else:
            self.__config_param["app"]["attendance_by_dni"] = "False"
        if self.__rb_user_name.get_active():
            self.__config_param["app"]["attendance_by_user_name"] = "True"
        else:
            self.__config_param["app"]["attendance_by_user_name"] = "False"
        if self.__op_chb_events.get_active():
            self.__config_param["app"]["events_attendance"] = "True"
        else:
            self.__config_param["app"]["events_attendance"] = "False"

        # Save finger print options
        if self.__r_right_hand.get_active():
            self.__config_param["finger_print"]["hand"] = "right"
        else:
            self.__config_param["finger_print"]["hand"] = "left"
        if self.__r_thumb_finger.get_active():
            self.__config_param["finger_print"]["finger"] = "thumb"
        elif self.__r_index_finger.get_active():
            self.__config_param["finger_print"]["finger"] = "index"
        elif self.__r_middle_finger.get_active():
            self.__config_param["finger_print"]["finger"] = "middle"
        elif self.__r_ring_finger.get_active():
            self.__config_param["finger_print"]["finger"] = "ring"
        elif self.__r_little_finger.get_active():
            self.__config_param["finger_print"]["finger"] = "little"

        ok_save = self.__config_manager.save_configurations(self.__config_param)
        if not ok_save:
            self.__show_dialog(gtk.MESSAGE_ERROR,_("Error trying to save settings"))
        else:
            self.__show_dialog(gtk.MESSAGE_INFO,_("The settings are saved correctly!"))
            if changed_db_parameters:
                self.__show_dialog(gtk.MESSAGE_INFO,_("You must restart the application for the changes to be applied"))
