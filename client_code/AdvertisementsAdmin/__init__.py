from ._anvil_designer import AdvertisementsAdminTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Home import Home
# from ..AdvertisementEdit import AdvertisementEdit
from anvil_extras import routing

@routing.route('advertisementadmin')
class AdvertisementsAdmin(AdvertisementsAdminTemplate):
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
    self.refresh_advertisement()

    # Any code you write here will run before the form opens.

  def refresh_advertisement(self):
    if anvil.users.get_user()['admin']:
      waitAdRows, availableSlots = anvil.server.call('get_waiting_advertisement')
      self.label_availability.text = availableSlots
      if len(waitAdRows) > 0:
        self.repeating_panel_waiting_ads.items = waitAdRows
        self.column_panel_no_waiting_ads.visible = False
        self.repeating_panel_waiting_ads.visible = True
      else:
        self.repeating_panel_waiting_ads.visible = False
        self.column_panel_no_waiting_ads.visible = True
      acceptedAdRows = anvil.server.call('get_accepted_advertisement')
      if len(acceptedAdRows) > 0:
        self.repeating_panel_accepted_ads.items = acceptedAdRows
        self.column_panel_no_accepted_ads.visible = False
        self.repeating_panel_accepted_ads.visible = True
      else:
        self.repeating_panel_accepted_ads.visible = False
        self.column_panel_no_accepted_ads.visible = True
      approvedAdRows = anvil.server.call('get_approved_advertisement')
      if len(approvedAdRows) > 0:
        self.repeating_panel_approved_ads.items = approvedAdRows
        self.column_panel_no_approved_ads.visible = False
        self.repeating_panel_approved_ads.visible = True
      else:
        self.repeating_panel_approved_ads.visible = False
        self.column_panel_no_approved_ads.visible = True
    else:
      homepage = get_open_form()
      homepage.content_panel.clear()
      homepage.content_panel.add_component(Home())
      anvil.users.logout()
      

