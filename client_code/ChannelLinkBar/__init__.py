from ._anvil_designer import ChannelLinkBarTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..LinkEdit import LinkEdit

class ChannelLinkBar(ChannelLinkBarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()
    # Any code you write here will run before the form opens.

  def refresh(self):
    if self.item['socialMediaName'] == 'YouTube':
      self.image_logo.source = '_/theme/Youtube_logo.png'
    elif self.item['socialMediaName'] == 'Instagram':
      self.image_logo.source = '_/theme/Instagram_logo.png'
    elif self.item['socialMediaName'] == 'Fiverr':
      self.image_logo.source = '_/theme/fiverr.png'
    elif self.item['socialMediaName'] == 'Facebook':
      self.image_logo.source = '_/theme/Facebook.png'
    elif self.item['socialMediaName'] == 'X (Twitter)':
      self.image_logo.source = '_/theme/X_logo.png'
    elif self.item['socialMediaName'] == 'LinkedIn':
      self.image_logo.source = '_/theme/LinkedIn_Logo2.png'
    elif self.item['socialMediaName'] == 'Gmail':
      self.image_logo.source = '_/theme/Gmail_icon.png'
    elif self.item['socialMediaName'] == 'PayPal':
      self.image_logo.source = '_/theme/Paypal_logo.png'

