from ._anvil_designer import LinkEditTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class LinkEdit(LinkEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.setConfig()
    # Any code you write here will run before the form opens.
    self.drop_down_platform.items = ['YouTube', 'Instagram', 'Fiverr', 'Facebook', 'X (Twitter)', 'LinkedIn', 'Gmail', 'PayPal']

  @property
  def mode(self):
    return self._mode

  @mode.setter
  def mode(self, value):
    self._mode = value

  @property
  def socialmedianame(self):
    return self._socialmedianame

  @socialmedianame.setter
  def socialmedianame(self, value):
    self._socialmedianame = value

  @property
  def link(self):
    return self._link

  @link.setter
  def link(self, value):
    self._link = value

  def setConfig(self):
    if self._mode == 'create':
      self.label_panelTitle.text = 'Create new link'
    elif self._mode == 'update':
      self.label_panelTitle.text = 'Update the link'
      self.drop_down_platform.selected_value = self._socialmedianame
      self.text_box_link.text = self._link
    else:
      print("Something wrong")

  def button_save_click(self, **event_args):
    """This method is called when the button is clicked"""
    self._socialmedianame = self.drop_down_platform.selected_value
    self._link = self.text_box_link.text
    if self._link == '':
      self.label_validation.text = 'Link is required.'
      self.column_panel_validation.visible = True
    else:
      self.column_panel_validation.visible = False
      link_dict = {'socialMediaName': self._socialmedianame, 'link': self._link}
      self.raise_event("x-close-alert", value=link_dict)
