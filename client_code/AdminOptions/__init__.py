from ._anvil_designer import AdminOptionsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AdminOptions(AdminOptionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_addAdmin_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event("x-close-alert", value='addAdmin')

  def button_blocked_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event("x-close-alert", value='blockedDubs')

  def button_allFlags_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event("x-close-alert", value='allFlags')

  def button_ads_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event('x-close-alert', value='adsAdmin')

  def button_top_ten_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event('x-close-alert', value='topTen')
    
