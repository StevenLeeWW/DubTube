from ._anvil_designer import FlagTemplate
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

@routing.route('flag')
class Flag(FlagTemplate):
  def __init__(self, **properties):
    if anvil.users.get_user() is None:
      loggedIn = get_open_form().checkLogin()
      print(loggedIn)
      if loggedIn:
        pass
      else:
        routing.set_url_hash('')
        routing.clear_cache()
        return None
    get_open_form().reset_links()
    get_open_form().link_flagged.role = 'selected'
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_flags()
    if 'Firefox' in str(navigator.userAgent):
      self.label_seekable.visible = False
      self.label_seekable2.visible = False
    

  def refresh_flags(self):
    self.refresh_raised_flags()
    self.refresh_received_flags()

  
  def refresh_raised_flags(self):
    myFlags = anvil.server.call('get_my_flags')
    if len(myFlags) > 0:
      self.column_panel_noRaisedFlag.visible = False
      self.repeating_panel_raisedFlags.items = myFlags
      self.repeating_panel_raisedFlags.visible = True
    else:
      self.repeating_panel_raisedFlags.visible = False
      self.column_panel_noRaisedFlag.visible = True

  def refresh_received_flags(self):
    user = anvil.users.get_user()
    if user['flagNewEmailNotification'] == True:
      self.label_stop_email.text = 'Want to stop receiving email notifications when new flag is received?'
      self.button_stop_email_notification.text = 'Stop receiving emails'
    else:
      self.label_stop_email.text = 'Want to continue receiving email notifications when new flag is received?'
      self.button_stop_email_notification.text = 'Continue receiving emails'
    receivedFlags = anvil.server.call('get_my_received_flags')
    if len(receivedFlags) > 0:
      self.column_panel_noReceivedFlag.visible = False
      self.repeating_panel_receivedFlags.items = receivedFlags
      self.repeating_panel_receivedFlags.visible = True
    else:
      self.repeating_panel_receivedFlags.visible = False
      self.column_panel_noReceivedFlag.visible = True

  def button_stop_email_notification_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    previousFlagNewEmail = True
    if user['flagNewEmailNotification'] == False:
      previousFlagNewEmail = False
    success = anvil.server.call('stop_continue_flag_email')
    if success:
      Notification('Email notification setting changed successfully.', style='success', title='Success').show()
      if previousFlagNewEmail == True:
        self.label_stop_email.text = 'Want to continue receiving email notifications when new flag is received?'
        self.button_stop_email_notification.text = 'Continue receiving emails'
      else:
        self.label_stop_email.text = 'Want to stop receiving email notifications when new flag is received?'
        self.button_stop_email_notification.text = 'Stop receiving emails'
    else:
      Notification('Something is wrong...', style='warning', title='Fail').show()
