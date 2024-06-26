from ._anvil_designer import FlagOptionsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class FlagOptions(FlagOptionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    

  def button_update_click(self, **event_args):
    """This method is called when the 'update' button is clicked"""
    self.raise_event("x-close-alert", value='update')

  
  def button_delete_click(self, **event_args):
    """This method is called when the 'delete' button is clicked"""
    self.raise_event("x-close-alert", value='delete')

