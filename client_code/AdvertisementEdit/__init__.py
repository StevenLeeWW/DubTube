from ._anvil_designer import AdvertisementEditTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AdvertisementEdit(AdvertisementEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.setConfig()
    # Any code you write here will run before the form opens.


  @property
  def mode(self):
    return self._mode

  @mode.setter
  def mode(self, value):
    self._mode = value

  @property
  def link(self):
    return self._link

  @link.setter
  def link(self, value):
    self._link = value

  @property
  def advertisementpicture(self):
    return self._advertisementpicture

  @advertisementpicture.setter
  def advertisementpicture(self, file):
    self._advertisementpicture = file

  
  def setConfig(self):
    if self._mode == 'create':
      self.label_panel_title.text = 'Apply for new ad placement'
    elif self._mode == 'update':
      self.label_panel_title.text = 'Update the ad placement application'
      self.text_box_link.text = self._link
    else:
      print("Something wrong")
    

  def file_loader_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file is not None:
      if file.content_type != 'image/jpg' and file.content_type != 'image/png' and file.content_type != 'image/jpeg':
        self.label_validation.text = 'Please upload an image file in jpg or png format.'
        self.column_panel_validation.visible = True
      else:
        self.column_panel_validation.visible = False
        self._advertisementpicture = file
    else:
      self.label_validation.text = 'Please upload a picture for your advertisement.'
      self.column_panel_validation.visible = True
    

  def button_save_click(self, **event_args):
    """This method is called when the button is clicked"""
    self._link = self.text_box_link.text
    if self._link == '':
      self.label_validation.text = 'Link is required.'
      self.column_panel_validation.visible = True
      return None
    if self._advertisementpicture is None:
      self.label_validation.text = 'Please upload a picture for your advertisement.'
      self.column_panel_validation.visible = True
      return None
    if self._advertisementpicture.content_type != 'image/jpg' and self.advertisementpicture.content_type != 'image/png' and self.advertisementpicture.content_type != 'image/jpeg':
      self.label_validation.text = 'Please upload an image file in jpg or png format.'
      self.column_panel_validation.visible = True
      return None
    self.column_panel_validation.visible = False
    ad_dict = {'link': self._link, 'advertisementPicture': self._advertisementpicture}
    self.raise_event("x-close-alert", value=ad_dict)
    
