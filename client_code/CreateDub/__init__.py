from ._anvil_designer import CreateDubTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
from anvil_extras import routing


@routing.route('create')
class CreateDub(CreateDubTemplate):
  def __init__(self, **properties):
    # Any code you write here will run before the form opens.
    # Check whether user is logged in
    if anvil.users.get_user() is None:
      loggedIn = get_open_form().checkLogin()
      if loggedIn:
        pass
      else:
        # Go to home if not logged in
        routing.set_url_hash('')
        routing.clear_cache()
        return None
    try:
      if properties['videourl'] != '':
        pass
    except Exception:
      properties['videourl'] = ''
    get_open_form().reset_links()
    get_open_form().link_create.role = 'selected'
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    languagesList = ['Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
    languagesCodeList = ['af', 'ak', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bn', 'eu', 'be', 'bho', 'bs', 'bg', 'my', 'ca', 'ceb', 'zh-Hans', 'co', 'hr', 'cs', 'da', 'dv', 'nl', 'en', 'eo', 'et', 'ee', 'fil', 'fi', 'fr', 'gl', 'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jv', 'kn', 'kk', 'km', 'rw', 'ko', 'kri', 'ku', 'ky', 'lo', 'la', 'lv', 'ln', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'ne', 'nso', 'no', 'ny', 'or', 'om', 'ps', 'fa', 'pl', 'pt', 'pa', 'qu', 'ro', 'ru', 'sm', 'sa', 'gd', 'sr', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'st', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'ti', 'ts', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'fy', 'xh', 'yi', 'yo', 'zu']
    self.drop_down_language.items = list(zip(languagesList, languagesCodeList))
    # Map the language code to the language
    self.languages_mapping = {code: language for language, code in zip(languagesList, languagesCodeList)}
    
    speakerList = ['Follow', 'Male 1', 'Female 1', 'Male 2', 'Female 2', 'Male 3', 'Female 3', 'Male 4', 'Female 4', 'Male 5', 'Female 5', 'Male 6', 'Female 6']
    speakerCodeList = ['', 'm1', 'f1', 'm2', 'f2', 'm3', 'f3', 'm4', 'f4', 'm5', 'f5', 'm6', 'f6']
    self.drop_down_newSpeaker_trans.items = list(zip(speakerList, speakerCodeList))
    
    self.drop_down_accent.items = ["Afghanistan", "Azerbaijan", "Bangladesh", "Belgium", "Burundi", "Chad", "China", "Czech Republic", "Ethiopia", "France", "Germany", "India", "Indonesia", "Iran", "Iraq", "Israel", "Italy", "Japan", "Kashmir", "Kosovo", "Kyrgyzstan", "Lesotho", "Madagascar", "Malawi", "Malaysia", "Malta", "Mexico", "Montenegro", "Myanmar", "Nepal", "Netherlands", "Nigeria", "Pakistan", "Peru", "Philippines", "Poland", "Quebec", "Romania", "Russia", "Rwanda", "Senegal", "Serbia", "Slovakia", "Slovenia", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Swaziland", "Sweden", "Switzerland", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uzbekistan", "Yugoslavia", "Zimbabwe"]
    self.text_box_videoUrl.text = self._videourl
    # youTubeSubtitle = True


  @property
  def videourl(self):
    return self._videourl

  
  @videourl.setter
  def videourl(self, value):
    self._videourl = value


  def search(self):
    """Search for the video using url"""
    videoUrl = self.text_box_videoUrl.text
    if self.text_box_videoUrl.text != '':
      videoID = anvil.server.call('get_video_id_from_url', self.text_box_videoUrl.text)
      if videoID is not None:
        youTubeVideoTitle = anvil.server.call('get_video_title_from_url', videoUrl)
        if youTubeVideoTitle is not None:
          self.item['youTubeVideoID'] = videoID
          self._videourl = 'https://www.youtube.com/watch?v=' + videoID
          self.item['videoTitle'] = youTubeVideoTitle
          self.youtube_video.youtube_id = videoID
          self.column_panel_invalid_url.visible = False
          self.column_panel_YTvideo.visible = True
        else:
          self.column_panel_YTvideo.visible = False
          self.column_panel_invalid_url.visible = True
          self.button_transcript.visible = False
      else:
        self.column_panel_YTvideo.visible = False
        self.column_panel_invalid_url.visible = True
        self.button_transcript.visible = False

  
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
    self.button_transcript.visible = True
    self.column_panel_video_confirmed.visible = True
    self.column_panel_skip_transcript.visible = True

  
  def button_no_click(self, **event_args):
    """This method is called when the 'no' button is clicked"""
    self.text_box_videoUrl.enabled = True
    self.button_search.enabled = True
    self.column_panel_video_confirmed.visible = False
    self.column_panel_skip_transcript.visible = False


  def button_transcript_click(self, **event_args):
    """This method is called when the 'get original language transcript' button is clicked"""
    self.column_panel_transcript.visible = False
    self.flow_panel_after_transcript.visible = False
    # Call 'get_transcript' function in Google Colab Notebook
    transcript = anvil.server.call('get_transcript', self._videourl, 'original')
    # If the transcript is a dictionary
    if isinstance(transcript, dict):
      # If there are multiple transcripts
      if transcript['multiple'] == 'yes':
        self.column_panel_ori_transcript_choice.visible = True
        options = transcript['options']
        # Let the multiple transcript options be the drop down list items
        self.drop_down_multiple_ori_transcript.items = options
        self.drop_down_multiple_ori_transcript.enabled = True
        return None
      else:
        Notification('Something is wrong...', style='warning', title='Alert').show()
    else:
      # If the returned transcript is not a dictionary
      self.column_panel_ori_transcript_choice.visible = False
      self.drop_down_multiple_ori_transcript.enabled = False
    # If there is no YouTube transcript
    if transcript == []:
      self.button_YT_translated.visible = False
      with Notification('Transcript not found in YouTube. Transcription is needed. Please wait...'):
        # Call the transcribe function in Google Colab Notebook
        transcript = anvil.server.call('transcribe', self._videourl, self.item['videoTitle'])
        # Upload the separated accompaniment to database
        anvil.server.call('upload_accompaniment_vocal', self._videourl, self.item['videoTitle'])
    else:
      # If there is a YouTube transcript
      self.button_YT_translated.visible = True
    self.repeating_panel_transcript.items = transcript
    self.column_panel_transcript.visible = True
    self.flow_panel_after_transcript.visible = True
    self.item['languageCode'] = self.drop_down_language.selected_value
    self.text_box_language.text = self.languages_mapping.get(self.item['languageCode'])

  
  def button_save_click(self, **event_args):
    """This method is called when the 'save' button in the translation is clicked"""
    translation = self.repeating_panel_translation.items
    # Make sure the times are integers
    for line in translation:
      try:
        line['startMin'] = int(line['startMin'])
        line['startSec'] = int(line['startSec'])
        line['endMin'] = int(line['endMin'])
        line['endSec'] = int(line['endSec'])
      except Exception:
        Notification('Timing should be entered as integer!', style='warning', title='Alert').show()
        return False
      if line['startMin'] == '':
        Notification('Starting minute cannot be empty!', style='warning', timeout=3).show()
        return False
      if line['startSec'] == '':
        Notification('Starting second cannot be empty!', style='warning', timeout=3).show()
        return False
      if line['endMin'] == '':
        Notification('Ending minute cannot be empty!', style='warning', timeout=3).show()
        return False
      if line['endSec'] == '':
        Notification('Ending second cannot be empty!', style='warning', timeout=3).show()
        return False
    success = anvil.server.call('save_transcript', self.item['youTubeVideoID'], self.item['videoTitle'], self.item['languageCode'], translation)
    if success:
      Notification('Saved successfully', style='success').show()
      return True
    else:
      Notification('Something is wrong', style='warning').show()
      return False

  
  def button_save_continue_click(self, **event_args):
    """This method is called when the 'save and continue' button is clicked"""
    # Trigger the button_save_click() method
    transcriptSaved = self.button_save_click()
    if not transcriptSaved:
      return False
    # Check whether accompaniment is saved in database
    if anvil.server.call('check_accompaniment', self.item['youTubeVideoID']):
      pass
    else:
      with Notification('Separating audio into vocal and accompaniment. Please wait...'):
        anvil.server.call('combineAudio', self._videourl)
        anvil.server.call('upload_accompaniment_vocal', self._videourl, self.item['videoTitle'])
    self.column_panel_generate.visible = True
    # Check whether unpublished dub exists
    transcriptRow = anvil.server.call('check_temp_dub', self.item['languageCode'], self.item['youTubeVideoID'])
    # If exists
    if transcriptRow is not None:
      self.repeating_panel_tempDub.items = [transcriptRow]
      self.column_panel_tempDub.visible = True
      self.column_panel_noTempDub.visible = False
    else:
      self.column_panel_tempDub.visible = False
      self.column_panel_noTempDub.visible = True

  
  def button_add_click(self, **event_args):
    """This method is called when the 'add line' button is clicked"""
    # Get the current page number of the data grid
    dataGridPageNum = self.data_grid_transcript.get_page()
    # Create a dictionary to store the info of the line
    newLine = {'speaker': '', 'startMin': self.text_box_startMinAdd.text, 'startSec': self.text_box_startSecAdd.text, 'endMin': self.text_box_endMinAdd.text, 'endSec': self.text_box_endSecAdd.text, 'text': self.text_box_textAdd.text}
    if newLine['startMin'] == '':
      Notification('Starting minute cannot be empty!', style='warning', timeout=3).show()
      return False
    if newLine['startSec'] == '':
      Notification('Starting second cannot be empty!', style='warning', timeout=3).show()
      return False
    if newLine['endMin'] == '':
      Notification('Ending minute cannot be empty!', style='warning', timeout=3).show()
      return False
    if newLine['endSec'] == '':
      Notification('Ending second cannot be empty!', style='warning', timeout=3).show()
      return False
    tempNewLine = {'start': newLine['startMin']*60 + newLine['startSec'], **{k: v for k, v in newLine.items() if k != 'startMin' and k != 'startSec'}}
    if tempNewLine['start'] > (newLine['endMin']*60 + newLine['endSec']):
      Notification('End time must be later than start time!', style='warning', timeout=3).show()
      return False
    # Get the current transcript
    transcript = self.repeating_panel_transcript.items
    # Temporary convert the starting minute and starting second into second unit
    tempTranscript = [{'start': item['startMin'] * 60 + item['startSec'], **{k: v for k, v in item.items() if k != 'startMin' and k != 'startSec'}} for item in transcript]
    # Add the new line into the temporary transcript
    tempTranscript.append(tempNewLine)
    # Sort the temporary transcript based on the start value
    tempTranscript.sort(key=lambda x: x['start'])
    # Turn the start time back into start minutes and start seconds
    transcript = [{'startMin': item['start'] // 60, 'startSec': item['start'] % 60, **{k: v for k, v in item.items() if k != 'start'}} for item in tempTranscript]
    # Assign the transcript back into the repeating panel
    self.repeating_panel_transcript.items = transcript
    # Go to the working page
    self.data_grid_transcript.set_page(dataGridPageNum)
    # Clear all the info in the new line
    self.text_box_startMinAdd.text = ''
    self.text_box_startSecAdd.text = ''
    self.text_box_endMinAdd.text = ''
    self.text_box_endSecAdd.text = ''
    self.text_box_textAdd.text = ''


  def delete_line(self, line):
    """This method is called when the 'delete line' button in the transcript data grid is clicked"""
    # Get the transcript
    transcript = self.repeating_panel_transcript.items
    dataGridPageNum = self.data_grid_transcript.get_page()
    # Remove the line from the transcript
    transcript.remove(line)
    self.repeating_panel_transcript.items = transcript
    self.data_grid_transcript.set_page(dataGridPageNum)
  

  def delete_trans_line(self, line):
    """This method is called when the 'delete line' button in the translation data grid is clicked"""
    translation = self.repeating_panel_translation.items
    dataGridPageNum = self.data_grid_translation.get_page()
    translation.remove(line)
    self.repeating_panel_translation.items = translation
    self.data_grid_translation.set_page(dataGridPageNum)
    
  
  def button_generateDub_click(self, **event_args):
    """This method is called when the 'generate' button is clicked"""
    with Notification('Generating... Please wait...'):
      # Call the 'speak' function in the Google Colab Notebook
      success = anvil.server.call('speak', self.item['languageCode'], anvil.users.get_user(), self.item['youTubeVideoID'])    
    if success:
      Notification('Generated and uploaded.', style='success').show()
      # Get the unpublished dub from the database
      transcriptRow = anvil.server.call('check_temp_dub', self.item['languageCode'], self.item['youTubeVideoID'])
      self.repeating_panel_tempDub.items = [transcriptRow]
      self.column_panel_tempDub.visible = True
      self.column_panel_noTempDub.visible = False
    else:
      Notification('Something is wrong...', style='warning').show()

  
  def file_loader_tempDub_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.item['dub'] = file

  
  def button_uploadDub_click(self, **event_args):
    """This method is called when the 'upload' button is clicked"""
    fileExist = False
    try:
      file = self.item['dub']
      if file is not None:
        fileExist = True
    except Exception:
      Notification('No file is uploaded.', style='warning').show()
    if fileExist:
      success = anvil.server.call('add_upload_dub_to_transcript', self.item['languageCode'], self.item['youTubeVideoID'], self.item['dub'], self.drop_down_accent.selected_value)
      if success:
        Notification('Uploaded.', style='success').show()
        transcriptRow = anvil.server.call('check_temp_dub', self.item['languageCode'], self.item['youTubeVideoID'])
        self.repeating_panel_tempDub.items = [transcriptRow]
        self.column_panel_tempDub.visible = True
        self.column_panel_noTempDub.visible = False
      else:
        Notification('Something is wrong...', style='warning').show()

  
  def button_delete_click(self, **event_args):
    """This method is called when the 'delete unpublished dub' button is clicked"""
    if confirm("Do you want to delete the unpublished dub?"):
      success = anvil.server.call('delete_tempDub', self.item['languageCode'], self.item['youTubeVideoID'])
      if success:
        Notification('Deleted.', style='success').show()
        self.column_panel_tempDub.visible = False
        self.column_panel_noTempDub.visible = True
      else:
        Notification('Something is wrong...', style='warning').show()

  
  def button_publish_click(self, **event_args):
    """This method is called when the 'publish' button is clicked"""
    language = self.languages_mapping.get(self.item['languageCode'])
    dubExisted = anvil.server.call('check_dub_existed', self.item['languageCode'], self.item['youTubeVideoID'], language)
    if dubExisted:
      if confirm('You have a dub of this video in the same language and accent. Replace it?'):
        success = anvil.server.call('publish', self.item['languageCode'], self.item['youTubeVideoID'], language)
      else:
        return None
    else:
      success = anvil.server.call('publish', self.item['languageCode'], self.item['youTubeVideoID'], language)
    if success:
      Notification('Published!', style='success').show()
      homepage = get_open_form()
      homepage.link_content_click()
    elif not success:
      Notification('Something is wrong...', style='warning').show()
    

  def button_downloadTranscript_click(self, **event_args):
    """This method is called when the 'download transcript' button is clicked"""
    transcript = self.repeating_panel_transcript.items
    # Convert the transcript into anvil media
    transcriptMedia = anvil.server.call('convert_transcript_to_anvil_media', transcript)
    anvil.media.download(transcriptMedia)

  
  def button_deleteTranscript_click(self, **event_args):
    """This method is called when the 'delete transcript' button is clicked"""
    if confirm('Do you want to delete this transcript?'):
      self.column_panel_translation.visible = False
      self.button_save_continue.visible = False
      self.item['languageCode'] = self.drop_down_language.selected_value
      success = anvil.server.call('delete_transcript', self.item['languageCode'], self.item['youTubeVideoID'])
      if success:
        Notification('Translation deleted.', style='success').show()
      

  def file_loader_srt_change(self, file, **event_args):
    """This method is called when a new subtitle srt file is loaded into this FileLoader to load the info in the srt file into the datagrid"""
    try:
      self.column_panel_transcript.visible = False
      self.flow_panel_after_transcript.visible = False
      self.button_YT_translated.visible = False
      srt_file = file
      transcript_list = []
      # Decoding byte string to regular string
      lines = srt_file.get_bytes().decode().splitlines()
      i = 0
      while i < len(lines):
        line = lines[i].strip()
        if line.isdigit():
          i += 1  # Skip the number line
          time_line = lines[i].strip().split(" --> ")
          start_time = time_line[0].split(':')
          end_time = time_line[1].split(':')
          start_min = int(start_time[1])
          end_min = int(end_time[1])
          start_sec, start_mic_sec = map(int, start_time[2].split(',')[0:2])
          end_sec, end_mic_sec = map(int, end_time[2].split(',')[0:2])
          start_sec = round(start_sec + start_mic_sec/1000)
          end_sec = round(end_sec + end_mic_sec/1000)
          text = lines[i + 1].strip()
          transcript_list.append({
            'speaker': '',
            'startMin': start_min,
            'startSec': start_sec,
            'endMin': end_min,
            'endSec': end_sec,
            'text': text
          })
          i += 2
        else:
          i += 1
      self.repeating_panel_transcript.items = transcript_list
      self.column_panel_transcript.visible = True
      self.flow_panel_after_transcript.visible = True
    except Exception:
      Notification('Please upload valid srt file.', style='warning', title='Warning', timeout=3).show()
    self.item['languageCode'] = self.drop_down_language.selected_value
    self.text_box_language.text = self.languages_mapping.get(self.item['languageCode'])

  
  def button_clear_click(self, **event_args):
    """This method is called when the 'clear' button is clicked"""
    if confirm('Do you want to clear the transcript?'):
      self.repeating_panel_transcript.items = []
      self.text_box_startMinAdd.text = ''
      self.text_box_startSecAdd.text = ''
      self.text_box_endMinAdd.text = ''
      self.text_box_endSecAdd.text = ''
      self.text_box_textAdd.text = ''
      

  def button_YT_translated_click(self, **event_args):
    """This method is called when the 'YouTube translation' button is clicked"""
    self.column_panel_translation.visible = False
    self.button_save_continue.visible = False
    # Call the 'get_transcript' function in Google Colab Notebook
    transcript = anvil.server.call('get_transcript', self._videourl, self.item['languageCode'])
    if transcript == []:
      Notification('Something is wrong...', style='warning', title='Warning', timeout=3).show()
    else:
      self.repeating_panel_translation.items = transcript
      self.column_panel_translation.visible = True
      self.button_save_continue.visible = True
    

  def drop_down_language_change(self, **event_args):
    """This method is called when an item in the language drop down list is selected to select the target language"""
    self.item['languageCode'] = self.drop_down_language.selected_value
    self.text_box_language.text = self.languages_mapping.get(self.item['languageCode'])

  
  def button_translate_click(self, **event_args):
    """This method is called when the button is clicked"""
    transcript = self.repeating_panel_transcript.items
    self.column_panel_translation.visible = False
    self.button_save_continue.visible = False
    translation = anvil.server.call('translate_txt', transcript, self.item['languageCode'])
    if len(translation) > 0:
      self.repeating_panel_translation.items = translation
      self.column_panel_translation.visible = True
      self.button_save_continue.visible = True
    else:
      self.column_panel_translation.visible = False
      self.button_save_continue.visible = False
      Notification('Something is wrong...', style='warning', title='Warning', timeout=3).show()

  
  def file_loader_translation_change(self, file, **event_args):
    """This method is called when a new translation subtitle srt file is loaded into this FileLoader"""
    self.column_panel_translation.visible = False
    self.button_save_continue.visible = False
    srt_file = file
    transcript_list = []
    # Decoding byte string to regular string
    lines = srt_file.get_bytes().decode().splitlines()
    i = 0
    while i < len(lines):
      line = lines[i].strip()
      if line.isdigit():
        i += 1  # Skip the number line
        time_line = lines[i].strip().split(" --> ")
        start_time = time_line[0].split(':')
        end_time = time_line[1].split(':')
        start_min = int(start_time[1])
        end_min = int(end_time[1])
        start_sec, start_mic_sec = map(int, start_time[2].split(',')[0:2])
        end_sec, end_mic_sec = map(int, end_time[2].split(',')[0:2])
        start_sec = round(start_sec + start_mic_sec/1000)
        end_sec = round(end_sec + end_mic_sec/1000)
        text = lines[i + 1].strip()
        transcript_list.append({
          'speaker': '',
          'startMin': start_min,
          'startSec': start_sec,
          'endMin': end_min,
          'endSec': end_sec,
          'text': text
        })
        i += 2
      else:
        i += 1
    self.repeating_panel_translation.items = transcript_list
    self.column_panel_translation.visible = True
    self.button_save_continue.visible = True

  
  def button_downloadTranslation_click(self, **event_args):
    """This method is called when the 'download translation' button is clicked"""
    translation = self.repeating_panel_translation.items
    translationMedia = anvil.server.call('convert_transcript_to_anvil_media', translation)
    anvil.media.download(translationMedia)

  
  def button_add_translation_click(self, **event_args):
    """This method is called when the 'add line' button in the translation data grid is clicked"""
    # Get the current page number of the data grid
    dataGridPageNum = self.data_grid_translation.get_page()
    newLine = {'speaker': self.drop_down_newSpeaker_trans.selected_value, 'startMin': self.text_box_startMinAdd_trans.text, 'startSec': self.text_box_startSecAdd_trans.text, 'endMin': self.text_box_endMinAdd_trans.text, 'endSec': self.text_box_endSecAdd_trans.text, 'text': self.text_box_textAdd_trans.text}
    if newLine['startMin'] == '':
      Notification('Starting minute cannot be empty!', style='warning', timeout=3).show()
      return False
    if newLine['startSec'] == '':
      Notification('Starting second cannot be empty!', style='warning', timeout=3).show()
      return False
    if newLine['endMin'] == '':
      Notification('Ending minute cannot be empty!', style='warning', timeout=3).show()
      return False
    if newLine['endSec'] == '':
      Notification('Ending second cannot be empty!', style='warning', timeout=3).show()
      return False
    tempNewLine = {'start': newLine['startMin']*60 + newLine['startSec'], **{k: v for k, v in newLine.items() if k != 'startMin' and k != 'startSec'}}
    if tempNewLine['start'] > (newLine['endMin']*60 + newLine['endSec']):
      Notification('End time must be later than start time!', style='warning', timeout=3).show()
      return False
    translation = self.repeating_panel_translation.items
    tempTranslation = [{'start': item['startMin'] * 60 + item['startSec'], **{k: v for k, v in item.items() if k != 'startMin' and k != 'startSec'}} for item in translation]
    tempTranslation.append(tempNewLine)
    tempTranslation.sort(key=lambda x: x['start'])
    translation = [{'startMin': item['start'] // 60, 'startSec': item['start'] % 60, **{k: v for k, v in item.items() if k != 'start'}} for item in tempTranslation]
    self.repeating_panel_translation.items = translation
    self.data_grid_translation.set_page(dataGridPageNum)
    self.drop_down_newSpeaker_trans.selected_value = ''
    self.text_box_startMinAdd_trans.text = ''
    self.text_box_startSecAdd_trans.text = ''
    self.text_box_endMinAdd_trans.text = ''
    self.text_box_endSecAdd_trans.text = ''
    self.text_box_textAdd_trans.text = ''

  
  def file_loader_translation_skip_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.column_panel_transcript.visible = False
    self.flow_panel_after_transcript.visible = False
    self.spacer_after_transcript.visible = False
    self.file_loader_translation_change(file)

  
  def button_download_accompaniment_click(self, **event_args):
    """This method is called when the 'download accompaniment' button is clicked"""
    Notification('Please wait...', timeout=5).show()
    accompaniment = anvil.server.call('get_accompaniment', self._videourl)
    if accompaniment is not None:
      anvil.media.download(accompaniment)
    else:
      Notification('Something is wrong...', style='warning', title='Alert', timeout=3).show()

  
  def drop_down_newSpeaker_trans_change(self, **event_args):
    """This method is called when an item in the new speaker drop down list is selected"""
    pass

  
  def button_translation_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.spacer_after_transcript.visible = False
    self.column_panel_translation.visible = False
    self.button_save_continue.visible = False
    transcript = anvil.server.call('get_saved_transcript', self.drop_down_language.selected_value, self.item['youTubeVideoID'])
    if transcript is None:
      transcript = anvil.server.call('get_transcript', self._videourl, self.drop_down_language.selected_value)
    if transcript == []:
      self.button_YT_translated.visible = False
      with Notification('Transcript not found in YouTube. Transcription is needed. Please wait...'):
        transcript = anvil.server.call('transcribe', self._videourl, self.item['videoTitle'])
        anvil.server.call('upload_accompaniment_vocal', self._videourl, self.item['videoTitle'])
        self.repeating_panel_transcript.items = transcript
        self.item['languageCode'] = self.drop_down_language.selected_value
        self.text_box_language.text = self.languages_mapping.get(self.item['languageCode'])
        self.button_translate_click()
    else:
      self.button_YT_translated.visible = True
      self.repeating_panel_translation.items = transcript
      self.column_panel_translation.visible = True
      self.button_save_continue.visible = True
      self.item['languageCode'] = self.drop_down_language.selected_value
      self.text_box_language.text = self.languages_mapping.get(self.item['languageCode'])

  
  def button_saved_translation_click(self, **event_args):
    """This method is called when the 'get saved translation' button is clicked"""
    self.column_panel_translation.visible = False
    self.button_save_continue.visible = False
    transcript = anvil.server.call('get_saved_transcript', self.drop_down_language.selected_value, self.item['youTubeVideoID'])
    if transcript is None:
      Notification('No transcript saved in the target language.', style='warning', title='Alert', timeout=3).show()
    else:
      # self.button_YT_translated.visible = True
      self.repeating_panel_translation.items = transcript
      self.column_panel_translation.visible = True
      self.button_save_continue.visible = True
      self.item['languageCode'] = self.drop_down_language.selected_value
      self.text_box_language.text = self.languages_mapping.get(self.item['languageCode'])

  
  def drop_down_multiple_ori_transcript_change(self, **event_args):
    """This method is called when an item in the multiple transcript drop down list is selected"""
    # Get the language code of the selected language
    code = self.drop_down_multiple_ori_transcript.selected_value
    transcript = anvil.server.call('get_transcript', self._videourl, code)
    # If the transcript is a dictionary
    if isinstance(transcript, dict):
      if transcript['multiple'] == 'yes':
        self.column_panel_ori_transcript_choice.visible = True
        options = transcript['options']
        self.drop_down_multiple_ori_transcript.items = options
        return None
    if transcript == []:
      self.button_YT_translated.visible = False
      with Notification('Transcript not found in YouTube. Transcription is needed. Please wait...'):
        transcript = anvil.server.call('transcribe', self._videourl, self.item['videoTitle'])
        anvil.server.call('upload_accompaniment_vocal', self._videourl, self.item['videoTitle'])
    else:
      self.button_YT_translated.visible = True
    self.repeating_panel_transcript.items = transcript
    self.column_panel_transcript.visible = True
    self.flow_panel_after_transcript.visible = True
    self.item['languageCode'] = self.drop_down_language.selected_value
    self.text_box_language.text = self.languages_mapping.get(self.item['languageCode'])
    
  