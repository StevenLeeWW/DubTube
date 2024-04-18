from ._anvil_designer import ContentTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
from anvil.js.window import navigator
from anvil_extras import routing

@routing.route('content')
class Content(ContentTemplate):
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
    get_open_form().link_content.role = 'selected'
    self.today = datetime.now().date()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.drop_down_language.items = ['Any language', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.drop_down_accent.items = ["Any accent", "Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Machine", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
    self.repeating_panel.set_event_handler('x-delete-dub', self.delete_dub)
    self.refresh_contents()
    if 'Firefox' in str(navigator.userAgent):
      self.label_seekable.visible = False

  
  def refresh_contents_helper(self, contents):
    """Load dubs from the Data Table, and display them in the RepeatingPanel"""
    listOfDubs = contents[0]
    atLeastOneDub = contents[1]

    if len(listOfDubs) == 0:
      if atLeastOneDub:
        self.label_noContent.text = 'No content for selected filter parameters.'
        self.column_panel_noContent.visible = True
        self.repeating_panel.visible = False
      else:
        self.label_noContent.text = 'No content.'
        self.column_panel_noContent.visible = True
        self.repeating_panel.visible = False
    else:
      self.repeating_panel.items = listOfDubs
      self.column_panel_noContent.visible = False
      self.repeating_panel.visible = True
      

  def refresh_contents(self):
    """Load dubs from the Data Table, and display them in the RepeatingPanel"""
    self.text_box_searchContent.text = ''
    language = self.drop_down_language.selected_value
    accent = self.drop_down_accent.selected_value
    date = self.date_picker_filter.date
    user = anvil.users.get_user()
    contents = anvil.server.call('get_dubs', language, accent, None, user, date)
    self.refresh_contents_helper(contents)

  def date_picker_filter_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.refresh_contents()

  def drop_down_language_change(self, **event_args):
    """This method is called when an item is selected"""
    self.refresh_contents()

  def drop_down_accent_change(self, **event_args):
    """This method is called when an item is selected"""
    self.refresh_contents()

  def searchContent(self):
    if self.text_box_searchContent.text != '':
      if anvil.server.call('get_video_id_from_url', self.text_box_searchContent.text) is not None:
        videoUrl = self.text_box_searchContent.text
        keyword = ''
      else:
        videoUrl = ''
        keyword = self.text_box_searchContent.text
      dubRowsAtLeastOneDub = anvil.server.call('get_search_dubs', videoUrl, keyword)
      dubRows = dubRowsAtLeastOneDub[0]
      atLeastOneDub = dubRowsAtLeastOneDub[1]
      if atLeastOneDub:
        language = self.drop_down_language.selected_value
        accent = self.drop_down_accent.selected_value
        date = self.date_picker_filter.date
        user = anvil.users.get_user()
        contents = anvil.server.call('get_dubs', language, accent, None, user, date)
        listOfDubs = contents[0]
        atLeastOneContent = contents[1]
        if atLeastOneContent:
          relatedListOfDubs = []
          for dubRow in dubRows:
            if dubRow in listOfDubs:
              relatedListOfDubs.append(dubRow)
          contents = [relatedListOfDubs, atLeastOneContent]
          self.refresh_contents_helper(contents)
      else:
        contents = [[], False]
        self.refresh_contents_helper(contents)

  def text_box_searchContent_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.searchContent()

  def button_searchContent_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.searchContent()

  def button_showAll_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.drop_down_language.selected_value = 'Any language'
    self.drop_down_accent.selected_value = 'Any accent'
    self.date_picker_filter.date = datetime.now().date()
    self.refresh_contents()

  def delete_dub(self, audioRow, **event_args):
    deleteSuccessful = anvil.server.call('delete_audio', audioRow)
    if deleteSuccessful:
      Notification('Deleted successfully', style='success').show()
      self.refresh_contents()
    else:
      Notification('Deletion failed.', title='Warning', style='warning', timeout=3).show()