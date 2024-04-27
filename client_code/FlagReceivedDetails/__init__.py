from ._anvil_designer import FlagReceivedDetailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class FlagReceivedDetails(FlagReceivedDetailsTemplate):
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

  
  def setup(self):
    self.drop_down_reason.selected_value = self._flagreason
    self.text_area_details.text = '\n'.join([f"{i + 1}. {string}" for i, string in enumerate(self._flagdetails)])
