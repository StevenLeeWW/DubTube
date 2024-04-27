from ._anvil_designer import PublicRequestViewTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..DubEdit import DubEdit
from ..VideoPlayer import VideoPlayer


class PublicRequestView(PublicRequestViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.


  def checkLogin(self):
    homepage = get_open_form()
    return homepage.checkLogin()

  
  def button_create_click(self, **event_args):
    """This method is called when the 'create' button is clicked"""
    get_open_form().link_create.role = 'selected'
    loggedIn = self.checkLogin()
    if loggedIn:
      # currentUser = anvil.users.get_user()
      requestRow = dict(self.item)
      new_dub = {'videoUrl': requestRow['requestVideoUrl'], 'language': requestRow['requestLanguage'], 'accent': requestRow['requestAccent']}
      mode = {'mode': 'create'}
      save_clicked = alert(
        content=DubEdit(item=new_dub, **mode),
        large=True,
        buttons=[("Save", True), ("Cancel", False)],
      )
      if save_clicked:
        success = anvil.server.call('add_audio', new_dub)
        if success:
          Notification('New dub created successfully!', title='Success', style='success', timeout=3).show()
        else:
          Notification('Sorry. Fail to create new dub', title='Alert', style='warning', timeout=3).show()
    get_open_form().link_create.role = ''
    
