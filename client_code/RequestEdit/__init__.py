from ._anvil_designer import RequestEditTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RequestEdit(RequestEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.drop_down_language.items = ['Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.drop_down_accent.items = ["Any accent", "Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
    self.text_box_videoUrl.text = self._videourl


  @property
  def videourl(self):
    return self._videourl

  
  @videourl.setter
  def videourl(self, value):
    self._videourl = value

  
  def search(self):
    """Search for the video"""
    videoUrl = self.text_box_videoUrl.text
    if self.text_box_videoUrl.text != '':
      videoID = anvil.server.call('get_video_id_from_url', self.text_box_videoUrl.text)
      if videoID is not None:
        youTubeVideoTitle = anvil.server.call('get_video_title_from_url', videoUrl)
        if youTubeVideoTitle is not None:
          self.item['youTubeVideoID'] = videoID
          self.item['videoTitle'] = youTubeVideoTitle
          self.youtube_video.youtube_id = videoID
          self.column_panel_invalid_url.visible = False
          self.column_panel_YTvideo.visible = True
        else:
          self.column_panel_YTvideo.visible = False
          self.column_panel_invalid_url.visible = True
          self.button_request.visible = False
      else:
        self.column_panel_YTvideo.visible = False
        self.column_panel_invalid_url.visible = True
        self.button_request.visible = False

  
  def text_box_videoUrl_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.search()

  
  def button_search_click(self, **event_args):
    """This method is called when the 'search' button is clicked"""
    self.search()

  
  def button_yes_click(self, **event_args):
    """This method is called when the 'yes' button is clicked"""
    self.text_box_videoUrl.enabled = False
    self.button_search.enabled = False
    self.column_panel_language_accent.visible = True
    self.button_request.visible = True
    self.button_request.enabled = True

  
  def button_no_click(self, **event_args):
    """This method is called when the 'no' button is clicked"""
    self.text_box_videoUrl.enabled = True
    self.button_search.enabled = True
    self.column_panel_language_accent.visible = False
    self.button_request.enabled = False

  
  def drop_down_language_change(self, **event_args):
    """This method is called when an item in the language drop down list is selected"""
    self.button_request.enabled = True

  
  def button_request_click(self, **event_args):
    """This method is called when the 'request' button is clicked"""
    self.item['language'] = self.drop_down_language.selected_value
    self.item['accent'] = self.drop_down_accent.selected_value
    self.raise_event("x-close-alert", value=True)
    
    
    
    

  
        