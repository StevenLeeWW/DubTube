from ._anvil_designer import ProfileNameSetterTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ProfileNameSetter(ProfileNameSetterTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  
  def button_save_click(self, **event_args):
    """This method is called when the 'save' button is clicked"""
    profileName = self.text_box_profileName.text
    if profileName == '':
      self.label_validationMessage.text = 'Profile name is required.'
      self.column_panel_validation.visible = True
      return None
    if anvil.server.call('check_profile_name', profileName):
      self.column_panel_validation.visible = False
      self.raise_event("x-close-alert", value=profileName)
    else:
      self.label_validationMessage.text = 'The profile name has been taken. Please use another profile name.'
      self.column_panel_validation.visible = True
    
