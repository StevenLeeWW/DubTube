from ._anvil_designer import FlagInfoBarTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..DubView import DubView
from ..FlagEdit import FlagEdit

class FlagInfoBar(FlagInfoBarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    audioRow = self.item['audioRow']
    self.column_panel_dub.add_component(DubView(item=audioRow))
    self.column_panel_dub.get_components()[0].column_panel_1.role = 'default'

  def button_edit_click(self, **event_args):
    """This method is called when the button is clicked"""
    properties = {'mode': 'update', 'flagreason': self.item['flagReason'], 'flagdetails': self.item['flagDetails']}
    flag_dict = alert(
      content=FlagEdit(**properties),
      large=True,
      buttons=[('Cancel', -1)]
    )
    if flag_dict != -1:
      if anvil.server.call('flag_dub', self.item['audioRow'], flag_dict):
        Notification('Updated successfully', style='success').show()
        self.parent.parent.parent.refresh_raised_flags()
      else:
        Notification('Something is wrong...', style='warning').show()

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm('Do you want to remove the flag you raised for this dub?'):
      if anvil.server.call('delete_flag', self.item['audioRow']):
        Notification('Flag is removed.', style='success').show()
        self.parent.parent.parent.refresh_raised_flags()
      else:
        Notification('Something is wrong...', style='warning').show()
