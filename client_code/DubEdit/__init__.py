from ._anvil_designer import DubEditTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..CreateDub import CreateDub
from anvil_extras import routing


class DubEdit(DubEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.availableLanguages = ['Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.drop_down_language.items = self.availableLanguages
    self.availableCountries = ["Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Machine", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
    self.drop_down_accent.items = self.availableCountries
    self.setTitle()
    self.setUrl()

  
  @property
  def mode(self):
    return self._mode

  
  @mode.setter
  def mode(self, value):
    self._mode = value

  
  def setTitle(self):
    if self._mode == 'create':
      self.label_panelTitle.text = 'Create new dub'
    elif self._mode == 'update':
      self.label_panelTitle.text = 'Update the dub'
    else:
      Notification("Something wrong. Title cannot be set.", style='warning', title='Alert').show()

  
  def setUrl(self):
    if self._mode == 'update':
      self.text_box_videoUrl.text = self.item['videoUrl']['videoUrl']
      self.text_box_videoUrl.enabled = False

  
  def file_loader_uploadDub_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.item['audio'] = file

  
  def button_save_click(self, **event_args):
    """This method is called when the 'save' button is clicked"""
    if self.text_box_videoUrl.text == '':
      self.label_validationMessage.text = 'Video URL is required'
      self.column_panel_validation.visible = True
      return None
    videoUrl = self.text_box_videoUrl.text
    if anvil.server.call('get_video_id_from_url', videoUrl) is None or anvil.server.call('get_video_title_from_url', videoUrl) is None:
      self.label_validationMessage.text = 'Video URL is not valid.'
      self.column_panel_validation.visible = True
      return None
    try:
      audio = self.item['audio']
      if audio is not None:
        pass
    except Exception:
      self.label_validationMessage.text = 'Audio file is required'
      self.column_panel_validation.visible = True
      return None
    self.column_panel_validation.visible = False
    self.raise_event("x-close-alert", value=True)  

  
  def button_generate_click(self, **event_args):
    """This method is called when the 'advance' button is clicked"""
    if self.text_box_videoUrl.text == '':
      self.label_validationMessage.text = 'Video URL is required'
      self.column_panel_validation.visible = True
      return None
    videoUrl = self.text_box_videoUrl.text
    # Check whether the video url is valid
    if anvil.server.call('get_video_id_from_url', videoUrl) is None or anvil.server.call('get_video_title_from_url', videoUrl) is None:
      self.label_validationMessage.text = 'Video URL is not valid.'
      self.column_panel_validation.visible = True
      return None
    properties = {'videourl': videoUrl}
    routing.set_url_hash(url_pattern='create', **properties)
    self.raise_event("x-close-alert", value=False)
    
    


