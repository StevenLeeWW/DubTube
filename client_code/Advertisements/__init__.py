from ._anvil_designer import AdvertisementsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..AdvertisementEdit import AdvertisementEdit
from anvil_extras import routing

@routing.route('advertisement')
class Advertisements(AdvertisementsTemplate):
  def __init__(self, **properties):
    if anvil.users.get_user() is None:
      loggedIn = get_open_form().checkLogin()
      # print(loggedIn)
      if loggedIn:
        if anvil.users.get_user()['admin'] == False:
          pass
        else:
          routing.set_url_hash('')
          routing.clear_cache()
          return None
      else:
        routing.set_url_hash('')
        routing.clear_cache()
        return None
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_advertisement()

    # Any code you write here will run before the form opens.

  def refresh_advertisement(self):
    anvil.server.call('mark_ads_as_read')
    adRows, availableSlots = anvil.server.call('get_advertisement')
    self.label_availability.text = availableSlots
    if availableSlots == 0:
      self.button_apply.enabled = False
    if len(adRows) > 0:
      self.repeating_panel_ads.items = adRows
      self.column_panel_no_ads.visible = False
      self.repeating_panel_ads.visible = True
    else:
      self.repeating_panel_ads.visible = False
      self.column_panel_no_ads.visible = True
    
  
  def button_apply_click(self, **event_args):
    """This method is called when the button is clicked"""
    mode = {'mode': 'create'}
    new_ad = alert(
      content=AdvertisementEdit(**mode),
      large=True,
      buttons=[("Cancel", -1)],
    )
    if new_ad != -1:
      success = anvil.server.call('add_advertisement', new_ad)
      if success:
        Notification('New advertisement application created successfully!', title='Success', style='success', timeout=3).show()
        self.refresh_advertisement()
      else:
        Notification('Sorry. There are no available slots. Please try again later. Thank you.', title='Alert', style='warning', timeout=3).show()
    pass
