from ._anvil_designer import RequestsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
from anvil_extras import routing

@routing.route('request')
class Requests(RequestsTemplate):
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
    self.today = datetime.now().date()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.drop_down_language.items = ['Any language', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.drop_down_accent.items = ["Any accent", "Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
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
    user = anvil.users.get_user()
    if user['requestResponseEmailNotification'] == True:
      self.label_stop_email.text = 'Want to stop receiving email notification when someone responded to your request?'
      self.button_stop_email.text = 'Stop receiving emails'
    else:
      self.label_stop_email.text = 'Want to continue receiving email notification when someone responded to your request?'
      self.button_stop_email.text = 'Continue receiving emails'
    language = self.drop_down_language.selected_value
    accent = self.drop_down_accent.selected_value
    date = self.date_picker_filter.date
    user = anvil.users.get_user()
    # print('bbbbbbbbb')
    requests = anvil.server.call('get_requests', language, accent, None, user, date)
    self.refresh_requests_helper(requests)

  def button_clearRequest_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm(title='Warning', content='Do you want to clear all your requests?'):
      anvil.server.call('clear_request')
      self.refresh_requests()
      clearRequestsNote = Notification('All requests have been cleared.').show()

  def date_picker_filter_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.refresh_requests()
    dateToday = datetime.today()
    dateOneYearAgo = dateToday - timedelta(days=365)
    if self.date_picker_filter.date < dateOneYearAgo:
      dateFilterNote = Notification('Records older than 60 days might have been deleted by system.', style='warning', timeout=3, title='Attention')
      dateFilterNote.show()

  def drop_down_language_change(self, **event_args):
    """This method is called when an item is selected"""
    self.refresh_requests()

  def drop_down_accent_change(self, **event_args):
    """This method is called when an item is selected"""
    self.refresh_requests()

  def searchRequests(self):
    if self.text_box_searchRequest.text != '':
      if anvil.server.call('get_video_id_from_url', self.text_box_searchRequest.text) is not None:
        videoUrl = self.text_box_searchRequest.text
        keyword = ''
      else:
        videoUrl = ''
        keyword = self.text_box_searchRequest.text
      requests = anvil.server.call('get_search_requests', videoUrl, keyword, anvil.users.get_user())
      self.refresh_requests_helper(requests)
      

  def text_box_searchRequest_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.searchRequests()

  def button_searchRequest_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.searchRequests()

  def button_showAll_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.drop_down_language.selected_value = 'Any language'
    self.drop_down_accent.selected_value = 'Any accent'
    self.date_picker_filter.date = datetime.now().date()
    self.refresh_requests()

  def button_stop_email_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    previousRequestResponseEmail = True
    if user['requestResponseEmailNotification'] == False:
      previousRequestResponseEmail = False
    success = anvil.server.call('stop_continue_request_response_email')
    if success:
      Notification('Email notification setting changed successfully.', style='success', title='Success').show()
      if previousRequestResponseEmail == True:
        self.label_stop_email.text = 'Want to continue receiving email notification when someone responded to your request?'
        self.button_stop_email.text = 'Continue receiving emails'
      else:
        self.label_stop_email.text = 'Want to stop receiving email notification when someone responded to your request?'
        self.button_stop_email.text = 'Stop receiving emails'
    else:
      Notification('Something is wrong...', style='warning', title='Fail').show()
