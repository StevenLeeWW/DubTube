from ._anvil_designer import ChannelPictureTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ChannelPicture(ChannelPictureTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self._source = ''
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.

  @property
  def source(self):
    return self._source

  @property
  def width(self):
    return self._width

  @property
  def height(self):
    return self._height
  
  @source.setter
  def source(self, image):
    if image:
      self._source = image.url
      self.dom_nodes['imageSource'].src = image.url

  @width.setter
  def width(self, value):
    if value:
      self._width = value
      self.dom_nodes['imageSource'].width = value

  @height.setter
  def height(self, value):
    if value:
      self._height = value
      self.dom_nodes['imageSource'].height = value