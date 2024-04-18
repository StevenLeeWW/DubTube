from ._anvil_designer import VideoPlayerTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import time
from anvil.tables import app_tables
from anvil.js.window import navigator
from anvil.js.window import history
# from ..AudioPlayer import AudioPlayer
# from ..AudioPlayerVideoPlayerPage import AudioPlayerVideoPlayerPage
from ..RequestEdit import RequestEdit
from anvil_extras import routing

@routing.route('video', url_keys=['ytid', 'audioid', routing.ANY])
class VideoPlayer(VideoPlayerTemplate):
  def __init__(self, **properties):
    self.timer.interval = 0
    self.notOk = True
    try:
      # print('zero level')
      if properties['videourl'] != '' and properties['audioid'] != '' and properties['audio'] is not None:
        # print('first level')
        self.notOk = False
        pass
      else:
        # print('second level')
        properties = self.get_properties(properties)
        # print('third level')
        if properties is None:
          Notification('Invalid URL.', style='warning', title='Alert', timeout=3).show()
          return None
    except:
      # print('Bug bug bug')
      properties = self.get_properties(properties)
      if properties is None:
        Notification('Invalid URL.', style='warning', title='Alert', timeout=3).show()
        return None
    get_open_form().reset_links()
    # Set Form properties and Data Bindings.
    # self.item['pageName'] = 'videoPlayer'
    self.playFirstTime = True
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    
    self.drop_down_language.items = ['Any language', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    self.drop_down_accent.items = ["Any accent", "Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Machine", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
    self.video = anvil.server.call('get_video', self._videourl)
    self.youtube_video.youtube_id = self.video['youTubeVideoID']  
    self.label_videoTitle.text = self.video['videoTitle']
    # self.audio_player.source = self._audio
    # self.item['audio'] = anvil.server.call('get_first_audio', self.video)
    self.add_event_handler('x-refreshPage', self.refreshPage)
    # self.add_event_handler('x-refreshAudio', self.refresh_audio)
    self.add_event_handler('x-playVideo', self.playVideo)
    self.add_event_handler('x-pauseVideo', self.pauseVideo)
    self.transcript = None
    # self.timer = Timer(interval=1)
    # self.state = 'PAUSED'
    self.refreshPage()
    # self.refresh_audio()
    # self.highlightSelectedDub()
  
  @property
  def videourl(self):
    return self._videourl

  @videourl.setter
  def videourl(self, value):
    self._videourl = value

  @property
  def audio(self):
    return self._audio

  @audio.setter
  def audio(self, value):
    self._audio = value

  @property
  def audioid(self):
    return self._audioid

  @audioid.setter
  def audioid(self, value):
    self._audioid = value

  def get_properties(self, properties):
    try:
      videoid = routing.get_url_dict()['ytid']
      if anvil.server.call('check_videoid_exist', videoid):
        videourl = 'https://www.youtube.com/watch?v=' + videoid
        properties['videourl'] = videourl
      else:
        routing.set_url_hash('')
        routing.clear_cache()
        return None
      audioid = routing.get_url_dict()['audioid']
      properties['audioid'] = audioid
      audio = anvil.server.call('get_audio_from_id', audioid)
      if audio is not None:
        properties['audio'] = audio
        return properties
      else:
        # Notification('This channel does not exist.', title='Alert', style='warning', timeout=3).show()
        routing.set_url_hash('')
        routing.clear_cache()
        return None
    except:
      routing.set_url_hash('')
      routing.clear_cache()
      return None
  
  
  def refreshPage(self, **event_args):
    self.refresh_dubs()
    self.get_subtitle()
    self.highlightSelectedDub()
  
  def refresh_dubs(self):
    """Load existing dubs from the Data Table, and display them in the RepeatingPanel"""
    language = 'Any language'
    accent = 'Any accent'
    try:
      language = routing.get_url_dict()['language']
      self.drop_down_language.selected_value = language
    except:
      pass
    try:
      accent = routing.get_url_dict()['accent']
      self.drop_down_accent.selected_value = accent
    except:
      pass
    if language != 'Any language' or accent != 'Any accent':
      self.drop_down_language_accent_change()
    else:
      dubRows = anvil.server.call('get_video_player_dubs', self.video)
      unblockedDubRows = [dub for dub in dubRows if dub['blocked'] == False]
      self.repeating_panel.items = unblockedDubRows

  def get_subtitle(self):
    audioid = routing.get_url_dict()['audioid']
    self.transcript = anvil.server.call('get_subtitle', audioid)
  
  # def refresh_audio(self, audio, **event_args):
    # """Set the source of the audio player"""
    # self.audio_player.refresh_data_bindings()
    # self.column_panel_audioPlayer.clear()
    # audio_property = {'source': self._audio}
    # print(type(self._audio))
    # self.column_panel_audioPlayer.add_component(AudioPlayerVideoPlayerPage(**audio_property))
    # encoded_audio_data = base64.b64encode(audio.get_bytes()).decode('utf-8')
    # self.audio_player.dom_nodes['audioSource'].src = f'data:audio/wav;base64,{encoded_audio_data}'
    # self.audio_player.source(self._audio)
    
  def playVideo(self, **event_args):
    """Play the video"""
    self.youtube_video.play()

  def pauseVideo(self, **event_args):
    """Pause the video"""
    self.youtube_video.pause()

  def highlightSelectedDub(self):
    """Highlight the dubInfoBar with the same audio as the selected audio"""
    listOfDubInfoBars = self.repeating_panel.get_components()
    for dubInfoBar in listOfDubInfoBars:
      if dubInfoBar.item['audioID'] == self._audioid:
        dubInfoBar.column_panel_dubInfoBar.background = '#808080'
        dubInfoBar.column_panel_dubInfoBar.foreground = '#ffffff'
        dubInfoBar.link_playSelect.foreground = '#ffffff'
        dubInfoBar.label_channelName.foreground = '#ffffff'
        if 'Firefox' in str(navigator.userAgent):
          try:
            firstTime = routing.get_url_dict()['firefox']
            url_pattern = routing.get_url_pattern()
            url_dict = routing.get_url_dict()
            url_dict.pop('firefox')
            print(url_dict)
            query_string = ''
            for key, value in url_dict.items():
              if query_string:
                query_string += '&'
              query_string += f"{key}={value}"
            url_hash = '#' + url_pattern + '?' + query_string
            print(url_hash)
            history.replaceState({}, '', url_hash)
            print('success')
          except:
            if self.notOk:
              videoUrl = dubInfoBar.item['videoUrl']['videoUrl']
              videoID = dubInfoBar.item['videoUrl']['youTubeVideoID']
              audio = dubInfoBar.item['audio']
              audioID = dubInfoBar.item['audioID']
              video_properties = {'videourl': videoUrl, 'audio': audio, 'audioid': audioID}
              url_hash = routing.get_url_hash() + '&firefox=yes'
              print(url_hash)
              routing.clear_cache()
              routing.set_url_hash(url_hash, **video_properties)
        

  def drop_down_language_change(self, **event_args):
    """This method is called when an item is selected"""
    self.drop_down_language_accent_change()

  def drop_down_accent_change(self, **event_args):
    """This method is called when an item is selected"""
    self.drop_down_language_accent_change()
    
  def drop_down_language_accent_change(self):
    audioRows = anvil.server.call('get_video_player_dubs', self.video, self.drop_down_language.selected_value, self.drop_down_accent.selected_value)
    unblockedAudioRows = [audio for audio in audioRows if audio['blocked'] == False]
    if len(unblockedAudioRows) == 0:
      Notification('No available dub for selected dub language and accent', title='Notification', style='warning', timeout=3).show()
    else:
      self.repeating_panel.items = unblockedAudioRows
      # self.audio_player.source = None
      # self.playFirstTime = True
      # listOfDubInfoBars = self.repeating_panel.get_components()
      # for dubInfoBar in listOfDubInfoBars:
      #   self._audioid = dubInfoBar.item['audioID']
      #   self._audio = dubInfoBar.item['audio']
      #   self.refresh_audio(dubInfoBar.item['audio'])
      #   dubInfoBar.column_panel_dubInfoBar.background = '#808080'
      #   dubInfoBar.column_panel_dubInfoBar.foreground = '#ffffff'
      #   dubInfoBar.link_playSelect.foreground = '#ffffff'
      #   break


  def checkLogin(self):
    homepage = get_open_form()
    return homepage.checkLogin()

  
  def button_request_click(self, **event_args):
    """This method is called when the button is clicked"""
    loggedIn = self.checkLogin()
    if loggedIn:
      new_request = {}
      property = {'videourl': self._videourl}
      request = alert(
        content=RequestEdit(item=new_request, **property),
        large=True,
        buttons=[("Cancel", False)],
      )
      if request:
        message = anvil.server.call('add_request', new_request)
        if message == 'success':
          Notification('Request created successfully!', style='success').show()
        elif message == 'fail':
          Notification('Sorry. Request fail.', style='warning', timeout=3).show()
        elif message == 'exist':
          Notification('Requested in the past.', style='warning', timeout=3).show()

  
  def youtube_video_state_change(self, state, **event_args):
    """This method is called when the video changes state (eg PAUSED to PLAYING)"""
    # print(state, self.youtube_video.current_time)
    if state == 'PAUSED':
      self.audio_player.dom_nodes['audio'].pause()
      self.timer.interval = 0
    elif state == 'PLAYING':
      self.audio_player.dom_nodes['audio'].currentTime = self.youtube_video.current_time
      self.audio_player.dom_nodes['audio'].play()
      # self.state = 'PLAYING'
      # print(self.youtube_video.current_time)
      if self.transcript is not None:
        self.flow_panel_subtitle.visible = True
        self.spacer_subtitle.visible = True
        self.timer.interval = 1
          
      
  def get_text_at_time(self):
    for line in self.transcript:
      if line["start"] <= self.youtube_video.current_time <= line["end"]:
        self.label_subtitle.text = line["text"]
      # print("None")

  def timer_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.get_text_at_time()
    # pass
