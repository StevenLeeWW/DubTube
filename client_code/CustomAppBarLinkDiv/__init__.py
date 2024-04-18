from ._anvil_designer import CustomAppBarLinkDivTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CustomAppBarLinkDiv(CustomAppBarLinkDivTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @property
  def visible(self):
    return self._visible

  @visible.setter
  def visible(self, value):
    self._visible = value
    if value:
      self.dom_nodes['custom-container-component'].style.display = 'inline'
    else:
      self.dom_nodes['custom-container-component'].style.display = 'none'

  @property
  def width(self):
    return self._width

  @width.setter
  def width(self, value):
    self._width = value
    self.dom_nodes['custom-container-component'].style.width = value