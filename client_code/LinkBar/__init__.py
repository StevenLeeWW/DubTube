from ._anvil_designer import LinkBarTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..LinkEdit import LinkEdit

class LinkBar(LinkBarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()
    # Any code you write here will run before the form opens.

  def refresh(self):
    """Set the source of the logo image source based on the social media name"""
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

  
  def button_edit_click(self, **event_args):
    """This method is called when the 'edit' button is clicked"""
    parameters = {'mode': 'update', 'socialmedianame': self.item['socialMediaName'], 'link': self.item['link']}
    link_dict = alert(
      content=LinkEdit(**parameters),
      large=True,
      buttons=[("Cancel", -1)],
    )
    if link_dict != -1:
      success = anvil.server.call('update_link', self.item, link_dict)
      if success:
        Notification('Link updated successfully!', title='Success', style='success', timeout=3).show()
        self.parent.parent.parent.refresh_profile()
      else:
        Notification('Sorry. Fail to update the link', title='Alert', style='warning', timeout=3).show()

  def button_delete_click(self, **event_args):
    """This method is called when the 'delete' button is clicked"""
    if confirm('Are you sure you want to delete this link?', title='Warning'):
      self.parent.raise_event('x-delete-link', linkRow=self.item)
    


