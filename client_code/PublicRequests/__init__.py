from ._anvil_designer import PublicRequestsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
from anvil_extras import routing

@routing.route('publicrequest')
class PublicRequests(PublicRequestsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.today = datetime.now().date()
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.drop_down_language.items = ['Any language', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.drop_down_accent.items = ["Any accent", "Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
    self.drop_down_numberOfResults.items = ['10', '15', '20', '25', '30', '35', '40', '45', '50']
    self.refresh_requests()


  def refresh_requests_helper(self, requests):
    """Load existing requests from the Data Table, and display them in the RepeatingPanel"""
    requestRows = requests[0]
    numberOfRequest = requests[1]
    if len(requestRows) == 0:
      self.column_panel_noRequest.visible = True
      self.repeating_panel.visible = False
    else:
      self.repeating_panel.items = requestRows
      listOfRequestView = self.repeating_panel.get_components()
      counter = 0
      for requestView in listOfRequestView:
        youtube_id = anvil.server.call('get_video_id_from_url', requestRows[counter]['requestVideoUrl'])
        requestView.youtube_video.youtube_id = youtube_id
        requestView.label_request.text = str(numberOfRequest[counter])
        counter += 1
      self.column_panel_noRequest.visible = False
      self.repeating_panel.visible = True
  
  
  def refresh_requests(self):
    """Load existing requests from the Data Table, and display them in the RepeatingPanel"""
    selectedLanguage = self.drop_down_language.selected_value
    selectedAccent = self.drop_down_accent.selected_value
    selectedNumberOfResults = int(self.drop_down_numberOfResults.selected_value)
    date = self.date_picker.date
    requests = anvil.server.call('get_requests', selectedLanguage, selectedAccent, selectedNumberOfResults, None, date)
    self.refresh_requests_helper(requests)


  def drop_down_language_change(self, **event_args):
    """This method is called when an item is selected"""
    self.refresh_requests()

  
  def drop_down_accent_change(self, **event_args):
    """This method is called when an item is selected"""
    self.refresh_requests()

  
  def drop_down_numberOfResults_change(self, **event_args):
    """This method is called when an item is selected"""
    self.refresh_requests()

  def date_picker_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.refresh_requests()

  def text_box_search_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    if self.text_box_search.text != '':
      if anvil.server.call('get_video_id_from_url', self.text_box_search.text) is not None:
        videoUrl = self.text_box_search.text
        keyword = ''
      else:
        videoUrl = ''
        keyword = self.text_box_search.text
      requests = anvil.server.call('get_search_requests', videoUrl, keyword)
      self.refresh_requests_helper(requests)

  def button_search_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.text_box_search_pressed_enter()

  def button_showAll_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.refresh_requests()
