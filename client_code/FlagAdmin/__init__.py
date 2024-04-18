from ._anvil_designer import FlagAdminTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator
from anvil_extras import routing

@routing.route('flagadmin')
class FlagAdmin(FlagAdminTemplate):
  def __init__(self, **properties):
    if anvil.users.get_user() is None:
      loggedIn = get_open_form().checkLogin()
      print(loggedIn)
      if loggedIn:
        if anvil.users.get_user()['admin']:
          pass
        else:
          routing.set_url_hash('')
          routing.clear_cache()
          return None
      else:
        routing.set_url_hash('')
        routing.clear_cache()
        return None
    get_open_form().reset_links()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_received_flags()
    if 'Firefox' in str(navigator.userAgent):
      self.label_seekable.visible = False


  def refresh_received_flags(self):
    receivedFlags = anvil.server.call('get_flags_admin')
    if len(receivedFlags) > 0:
      self.column_panel_noReceivedFlag.visible = False
      self.repeating_panel_receivedFlags.items = receivedFlags
      self.repeating_panel_receivedFlags.visible = True
    else:
      self.repeating_panel_receivedFlags.visible = False
      self.column_panel_noReceivedFlag.visible = True
