from ._anvil_designer import CopyShareLinkTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator


class CopyShareLink(CopyShareLinkTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    

  def button_copy_click(self, **event_args):
    """This method is called when the 'copy' button is clicked"""
    link = self.text_box_link.text
    # Copy the link to clipboard
    navigator.clipboard.writeText(link)
    self.raise_event('x-close-alert', value=None)
    Notification('Link copied.', style='success', title='Success').show()
