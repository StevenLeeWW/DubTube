from ._anvil_designer import OptionsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Options(OptionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  
  def button_edit_click(self, **event_args):
    """This method is called when the 'edit' button is clicked"""
    self.raise_event("x-close-alert", value='edit')

  
  def button_delete_click(self, **event_args):
    """This method is called when the 'delete' button is clicked"""
    self.raise_event("x-close-alert", value='delete')

  def button_download_click(self, **event_args):
    """This method is called when the 'download' button is clicked"""
    self.raise_event("x-close-alert", value='download')
