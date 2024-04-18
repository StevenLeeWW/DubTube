from ._anvil_designer import TrendingTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Liked import Liked
from anvil.js.window import navigator
from anvil_extras import routing

@routing.route('trending')
class Trending(TrendingTemplate):
  def __init__(self, **properties):
    get_open_form().reset_links()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.drop_down_trendLanguage.items = ['Any language', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.drop_down_trendAccent.items = ["Any accent", "Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Machine", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
    self.drop_down_numberOfResults.items = ['10', '15', '20', '25', '30', '35', '40', '45', '50']
    self.refresh_dubs()
    if 'Firefox' in str(navigator.userAgent):
      self.label_seekable.visible = False


  def refresh_dubs(self):
    """Load existing dubs from the Data Table, and display them in the RepeatingPanel"""
    selectedLanguage = self.drop_down_trendLanguage.selected_value
    selectedAccent = self.drop_down_trendAccent.selected_value
    selectedNumberOfResults = int(self.drop_down_numberOfResults.selected_value)
    dubRows = anvil.server.call('get_dubs', selectedLanguage, selectedAccent, selectedNumberOfResults)
    unblockedDubRows = [dub for dub in dubRows if dub['blocked'] == False]
    self.repeating_panel_trending.items = unblockedDubRows

  def drop_down_change(self):
    selectedLanguage = self.drop_down_trendLanguage.selected_value
    selectedAccent = self.drop_down_trendAccent.selected_value
    selectedNumberOfResults = int(self.drop_down_numberOfResults.selected_value)
    dubRows = anvil.server.call('get_dubs', selectedLanguage, selectedAccent, selectedNumberOfResults)
    unblockedDubRows = [dub for dub in dubRows if dub['blocked'] == False]
    if len(unblockedDubRows) > 0:
      self.column_panel_noAvailableDubs.visible = False
      self.repeating_panel_trending.items = unblockedDubRows
    else:
      self.column_panel_noAvailableDubs.visible = True
      self.label_noAvailableDubs.text = 'Sorry. No available dubs for ' + selectedLanguage
      self.repeating_panel_trending.items = unblockedDubRows

    
  def drop_down_trendLanguage_change(self, **event_args):
    """This method is called when an item is selected"""
    self.drop_down_change()

  def drop_down_trendAccent_change(self, **event_args):
    """This method is called when an item is selected"""
    self.drop_down_change()

  def drop_down_numberOfResults_change(self, **event_args):
    """This method is called when an item is selected"""
    self.drop_down_change()
