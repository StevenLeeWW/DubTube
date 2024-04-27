from ._anvil_designer import LikedTemplate
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


@routing.route('liked')
class Liked(LikedTemplate):
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
    get_open_form().link_liked.role = 'selected'
    self.today = datetime.now().date()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_liked()
    # Any code you write here will run before the form opens.
    self.drop_down_language.items = ['Any language', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.drop_down_accent.items = ["Any accent", "Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Machine", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
    if 'Firefox' in str(navigator.userAgent):
      self.label_seekable.visible = False


  def refresh_liked(self):
    """Get existing liked dubs from the Data Table"""
    liked = anvil.server.call('get_liked')
    self.refresh_liked_helper(liked)
    
  
  def refresh_liked_helper(self, liked):
    """Get liked dubs, and display them in the RepeatingPanel"""
    likedAudios = liked[0]
    likedOns = liked[1]
    if len(likedAudios) == 0:
      self.column_panel_noLiked.visible = True
      self.repeating_panel.visible = False
    else:
      self.repeating_panel.items = likedAudios
      listOfLikedDubView = self.repeating_panel.get_components()
      counter = 0
      for likedDubView in listOfLikedDubView:
        likedDubView.label_date.text = 'Liked on: ' + str(likedOns[counter])
        counter += 1
      self.column_panel_noLiked.visible = False
      self.repeating_panel.visible = True

  
  def button_clearLiked_click(self, **event_args):
    """This method is called when the 'clear liked' button is clicked"""
    if confirm(title='Warning', content='Do you want to clear all your like-history?'):
      anvil.server.call('clear_liked')
      self.refresh_liked()
      Notification('All like-history have been cleared.', style='success', title='Success').show()

  
  def date_picker_filter_change(self, **event_args):
    """This method is called when the selected date changes"""
    liked = anvil.server.call('get_liked', self.date_picker_filter.date, self.drop_down_language.selected_value, self.drop_down_accent.selected_value)
    self.refresh_liked_helper(liked)

  
  def drop_down_language_change(self, **event_args):
    """This method is called when an item from the language drop down list is selected"""
    liked = anvil.server.call('get_liked', self.date_picker_filter.date, self.drop_down_language.selected_value, self.drop_down_accent.selected_value)
    self.refresh_liked_helper(liked)

  
  def drop_down_accent_change(self, **event_args):
    """This method is called when an item from the accent drop down list is selected"""
    liked = anvil.server.call('get_liked', self.date_picker_filter.date, self.drop_down_language.selected_value, self.drop_down_accent.selected_value)
    self.refresh_liked_helper(liked)

  
  def searchLiked(self):
    """Search the like dub"""
    if self.text_box_searchLiked.text != '':
      if anvil.server.call('get_video_id_from_url', self.text_box_searchLiked.text) is not None:
        videoUrl = self.text_box_searchLiked.text
        keyword = ''
      else:
        videoUrl = ''
        keyword = self.text_box_searchLiked.text
      dubRowsAtLeastOneDub = anvil.server.call('get_search_dubs', videoUrl, keyword)
      dubRows = dubRowsAtLeastOneDub[0]
      atLeastOneDub = dubRowsAtLeastOneDub[1]
      if atLeastOneDub:
        liked = anvil.server.call('get_liked')
        likedAudios = liked[0]
        likedOns = liked[1]
        relatedLikedAudios = []
        relatedLikedOns = []
        for dubRow in dubRows:
          if dubRow in likedAudios:
            relatedLikedAudios.append(dubRow)
            index = likedAudios.index(dubRow)
            relatedLikedOns.append(likedOns[index])
        liked = [relatedLikedAudios, relatedLikedOns]
        self.refresh_liked_helper(liked)
      else:
        liked = [[], []]
        self.refresh_liked_helper(liked)

  
  def text_box_searchLiked_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.searchLiked()

  
  def button_searchLiked_click(self, **event_args):
    """This method is called when the 'search' button is clicked"""
    self.searchLiked()

  
  def button_showAll_click(self, **event_args):
    """This method is called when the 'show all' button is clicked"""
    self.drop_down_language.selected_value = 'Any language'
    self.drop_down_accent.selected_value = 'Any accent'
    self.date_picker_filter.date = datetime.now().date()
    self.refresh_liked()
