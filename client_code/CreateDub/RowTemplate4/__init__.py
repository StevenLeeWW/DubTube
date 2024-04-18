from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    speakerList = ['Follow', 'Male 1', 'Female 1', 'Male 2', 'Female 2', 'Male 3', 'Female 3', 'Male 4', 'Female 4', 'Male 5', 'Female 5', 'Male 6', 'Female 6']
    speakerCodeList = ['', 'm1', 'f1', 'm2', 'f2', 'm3', 'f3', 'm4', 'f4', 'm5', 'f5', 'm6', 'f6']
    self.drop_down_speaker.items = list(zip(speakerList, speakerCodeList))
    # Any code you write here will run before the form opens.

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.parent.parent.parent.parent.delete_trans_line(self.item)
    
