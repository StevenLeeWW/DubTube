from ._anvil_designer import FlagEditTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class FlagEdit(FlagEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.setup()
    # Any code you write here will run before the form opens.
    self.drop_down_reason.items = ['It violates copyright', 'The content is inappropriate', 'It is not a dub.', 'Its quality is too bad.', 'The translation is inaccurate.', 'Others']

  @property
  def flagreason(self):
    return self._flagreason

  @flagreason.setter
  def flagreason(self, value):
    self._flagreason = value

  @property
  def flagdetails(self):
    return self._flagdetails

  @flagdetails.setter
  def flagdetails(self, value):
    self._flagdetails = value

  @property
  def mode(self):
    return self._mode

  @mode.setter
  def mode(self, value):
    self._mode = value

  def setup(self):
    if self._mode == 'create':
      self.label_title.text = 'Flag this dub'
    elif self._mode == 'update':
      self.label_title.text = 'Update the flag'
      self.drop_down_reason.selected_value = self._flagreason
      self.text_area_details.text = self._flagdetails

  def button_save_click(self, **event_args):
    """This method is called when the button is clicked"""
    returnDict = {'flagReason': self.drop_down_reason.selected_value, 'flagDetails': self.text_area_details.text[:200]}
    self.raise_event("x-close-alert", value=returnDict)
