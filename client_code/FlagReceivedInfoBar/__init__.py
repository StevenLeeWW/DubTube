from ._anvil_designer import FlagReceivedInfoBarTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..DubView import DubView
from ..FlagReceivedDetails import FlagReceivedDetails

class FlagReceivedInfoBar(FlagReceivedInfoBarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if anvil.users.get_user()['admin']:
      self.button_delete.visible = True
    else:
      self.button_delete.visible = False

    # Any code you write here will run before the form opens.
    audioRow = self.item[0]
    self.column_panel_dub.add_component(DubView(item=audioRow))
    self.column_panel_dub.get_components()[0].column_panel_1.role = 'default'
    if self.item[5] == False:
      self.column_panel.background = '#FFC300'

  def button_view_click(self, **event_args):
    """This method is called when the button is clicked"""
    properties = {'flagreason': self.item[1], 'flagdetails': self.item[4]}
    alert(
      content=FlagReceivedDetails(**properties),
      large=True,
      buttons=[('OK', True)]
    )
    if anvil.users.get_user()['admin'] == False:
      anvil.server.call('mark_flag_read', self.item[0], self.item[1])
    else:
      anvil.server.call('mark_flag_read_admin', self.item[0], self.item[1])
    self.column_panel.background = 'white'
    get_open_form().unread_flags_client()

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm('Do you want to delete the flags for this dub?'):
      audioRow = self.item[0]
      flagReason = self.item[1]
      success = anvil.server.call('delete_flags_admin', audioRow, flagReason)
      if success is None:
        anvil.users.logout()
        homepage = get_open_form()
        homepage.link_admin.visible = False
        homepage.showProfilePicture()
        Notification("You are logged out.").show()
        homepage.link_home_click()
        return
      if success:
        self.parent.parent.parent.refresh_received_flags()
      else:
        Notification('Something is wrong...', title='Error', style='warning').show()
    
