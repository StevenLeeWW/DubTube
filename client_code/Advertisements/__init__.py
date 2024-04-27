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
    # Any code you write here will run before the form opens.
    # If user is not logged in
    if anvil.users.get_user() is None:
      loggedIn = get_open_form().checkLogin()
      if loggedIn:
        # Non admin user can post advertisement applications
        if anvil.users.get_user()['admin'] == False:
          pass
        else:
          # Go back to home page if user is admin
          routing.set_url_hash('')
          routing.clear_cache()
          return None
      else:
        # Go back to homepage if user is not logged in
        routing.set_url_hash('')
        routing.clear_cache()
        return None
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_advertisement()
    

  def refresh_advertisement(self):
    """Prepare the info for the page"""
    # Change the advertisement applications' read status to true to change the appearance on the home page
    anvil.server.call('mark_ads_as_read')
    # Get the advertisement info and the number of remaining available slots
    adRows, availableSlots = anvil.server.call('get_advertisement')
    self.label_availability.text = availableSlots
    # If no more available slot, then cannot create new application
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
    """This method is called when the 'Plus' button is clicked"""
    mode = {'mode': 'create'}
    new_ad = alert(
      content=AdvertisementEdit(**mode),
      large=True,
      buttons=[("Cancel", -1)],
    )
    # If the 'Cancel' button is not clicked
    if new_ad != -1:
      success = anvil.server.call('add_advertisement', new_ad)
      if success:
        Notification('New advertisement application created successfully!', title='Success', style='success', timeout=3).show()
        self.refresh_advertisement()
      else:
        Notification('Sorry. There are no available slots. Please try again later. Thank you.', title='Alert', style='warning', timeout=3).show()
    pass
