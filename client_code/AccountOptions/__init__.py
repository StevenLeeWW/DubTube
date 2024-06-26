from ._anvil_designer import AccountOptionsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AccountOptions(AccountOptionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_profile_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event("x-close-alert", value='profile')

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event("x-close-alert", value='delete')

  def button_logOut_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event("x-close-alert", value='logout')
