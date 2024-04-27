from ._anvil_designer import AccountEditTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AccountEdit(AccountEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user = anvil.users.get_user()
    self.info = {}
    # Any code you write here will run before the form opens.


  def file_loader_uploadProfilePicture_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.info['profilePicture'] = file

  def button_update_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.info['profileName'] = self.text_box_profileName.text
    if self.info['profileName'] == '':
      self.label_validationMessage.text = 'Profile name is required.'
      self.column_panel_validation.visible = True
      return None
    # If the profile name has not been taken
    if anvil.server.call('check_profile_name', self.info['profileName']):
      self.column_panel_validation.visible = False
      self.info['profileDescription'] = self.text_area_profileDescription.text
      self.raise_event("x-close-alert", value=self.info)
    else:
      self.label_validationMessage.text = 'The profile name has been taken. Please use another profile name.'
      self.column_panel_validation.visible = True
    
