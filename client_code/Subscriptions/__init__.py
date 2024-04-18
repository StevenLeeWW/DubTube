from ._anvil_designer import SubscriptionsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import routing

@routing.route('subscription')
class Subscriptions(SubscriptionsTemplate):
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
    get_open_form().link_subscribed.role = 'selected'
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_subscription()
    get_open_form().new_released_not_listened_client()
    # Any code you write here will run before the form opens.

  
  def refresh_subscription(self):
    user = anvil.users.get_user()
    if user['subscriptionNewEmailNotification'] == True:
      self.label_stop_email.text = 'Want to stop receiving emails for new dubs?'
      self.button_stop_subscription_email.text = 'Stop receiving emails'
    else:
      self.label_stop_email.text = 'Want to continue receiving emails for new dubs?'
      self.button_stop_subscription_email.text = 'Continue receiving emails'
    subscriptions = anvil.server.call('get_subscriptions')
    if len(subscriptions[0]) == 0:
      self.column_panel_noSubscription.visible = True
      self.repeating_panel.visible = False
    else:
      self.repeating_panel.items = subscriptions[0]
      self.column_panel_noSubscription.visible = False
      self.repeating_panel.visible = True
      channelInfoBars = self.repeating_panel.get_components()
      for i in range(len(channelInfoBars)):
        if subscriptions[1][i]:
          channelInfoBars[i].label_new.visible = True
        else:
          channelInfoBars[i].label_new.visible = False

  
  def button_stop_subscription_email_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    previousSubscriptionNewEmail = True
    if user['subscriptionNewEmailNotification'] == False:
      previousSubscriptionNewEmail = False
    success = anvil.server.call('stop_continue_subscription_new_dub_email')
    if success:
      Notification('Email notification setting changed successfully.', style='success', title='Success').show()
      if previousSubscriptionNewEmail == True:
        self.label_stop_email.text = 'Want to continue receiving emails for new dubs?'
        self.button_stop_subscription_email.text = 'Continue receiving emails'
      else:
        self.label_stop_email.text = 'Want to stop receiving emails for new dubs?'
        self.button_stop_subscription_email.text = 'Stop receiving emails'
    else:
      Notification('Something is wrong...', style='warning', title='Fail').show()
