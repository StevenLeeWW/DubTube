from ._anvil_designer import ProfileTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..AccountEdit import AccountEdit
from ..LinkEdit import LinkEdit
from ..ProfileContent import ProfileContent
from ..EarnProfilePage import EarnProfilePage
from anvil_extras import routing

@routing.route('profile')
class Profile(ProfileTemplate):
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
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_profile()
    self.showContent()
    self.showEarn()
    # Any code you write here will run before the form opens.
    self.repeating_panel.set_event_handler('x-delete-link', self.delete_link)


  def showContent(self):
    self.column_panel_content.add_component(ProfileContent())


  def showEarn(self):
    self.column_panel_earn.add_component(EarnProfilePage())

  
  def refresh_profile(self):
    user = anvil.users.get_user()
    if user['profilePicture'] is not None:
      self.channel_picture.source = user['profilePicture']
    else:
      self.channel_picture.source = '_/theme/userDefault.jpg'
    self.label_profileName.text = user['profileName']
    self.label_subscribers.text = str(user['subscribers']) + ' subscribers'
    self.label_dubs.text = str(user['dubs']) + ' dubs'
    if user['profileDescription'] is None:
      self.label_description.text = 'None'
    else:
      self.label_description.text = user['profileDescription']
    links = anvil.server.call('get_links')
    if len(links) == 0:
      self.column_panel_noLinks.visible = True
      self.repeating_panel.visible = False
    else:
      self.column_panel_noLinks.visible = False
      self.repeating_panel.items = links
      self.repeating_panel.visible = True
    

  
  def button_editProfile_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    userRowCopy = dict(user)
    # print(userRowCopy)
    updatedUser = alert(
      content=AccountEdit(item=userRowCopy),
      # title = 'Update Dub',
      large=True,
      buttons=[("Cancel", None)],
    )
    if updatedUser is not None:
      # print(updatedUser)
      updateSuccessful = anvil.server.call('update_user', user, updatedUser)
      if updateSuccessful:
        Notification('Update successfully.', title='Alert', style='success').show()
        self.refresh_profile()
        get_open_form().showProfilePicture()
      else:
        Notification('Update fail.', title='Alert', style='warning', timeout=3).show()

  
  def button_deleteProfilePicture_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm('Are you sure you want to delete this profile picture?', title='Warning'):
      if anvil.server.call('delete_profilePicture', anvil.users.get_user()):
        Notification('Deleted successfully', style='success').show()
        self.refresh_profile()
        get_open_form().showProfilePicture()
      else:
        Notification('Deletion fail...', style='warning', timeout=3).show()

  
  def button_addLinks_click(self, **event_args):
    """This method is called when the button is clicked"""
    # new_link = {}
    mode = {'mode': 'create'}
    new_link = alert(
      content=LinkEdit(**mode),
      large=True,
      buttons=[("Cancel", -1)],
    )
    if new_link != -1:
      success = anvil.server.call('add_link', new_link)
      if success:
        Notification('New link created successfully!', title='Success', style='success', timeout=3).show()
        self.refresh_profile()
      else:
        Notification('Sorry. Fail to create new link', title='Alert', style='warning', timeout=3).show()
      
  def delete_link(self, linkRow, **event_args):
    deleteSuccessful = anvil.server.call('delete_link', linkRow)
    if deleteSuccessful:
      Notification('Link deleted successfully', style='success').show()
      self.refresh_profile()
    else:
      Notification('Link deletion failed.', title='Warning', style='warning', timeout=3).show()
  

