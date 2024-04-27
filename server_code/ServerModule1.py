import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta
from collections import Counter, OrderedDict
import anvil.media
import base64


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.


languagesList = ['Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azerbaijani', 'Bangla', 'Basque', 'Belarusian', 'Bhojpuri', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Ewe', 'Filipino', 'Finnish', 'French', 'Galician', 'Ganda', 'Georgian', 'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Krio', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Māori', 'Marathi', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian', 'Nyanja', 'Odia', 'Oromo', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Russian', 'Samoan', 'Sanskrit', 'Scottish Gaelic', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']
languagesCodeList = ['af', 'ak', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bn', 'eu', 'be', 'bho', 'bs', 'bg', 'my', 'ca', 'ceb', 'zh-Hans', 'co', 'hr', 'cs', 'da', 'dv', 'nl', 'en', 'eo', 'et', 'ee', 'fil', 'fi', 'fr', 'gl', 'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jv', 'kn', 'kk', 'km', 'rw', 'ko', 'kri', 'ku', 'ky', 'lo', 'la', 'lv', 'ln', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'ne', 'nso', 'no', 'ny', 'or', 'om', 'ps', 'fa', 'pl', 'pt', 'pa', 'qu', 'ro', 'ru', 'sm', 'sa', 'gd', 'sr', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'st', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'ti', 'ts', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'fy', 'xh', 'yi', 'yo', 'zu']
languages_mapping = {language: code for language, code in zip(languagesList, languagesCodeList)}


@anvil.server.callable
def make_admin(user):
  user.update(admin=True)


@anvil.server.callable
def add_user(email, password_hash, profileName):
  """Adding the necessary info after creating a user account"""
  newUser = app_tables.users.get(email=email)
  if newUser['password_hash'] == password_hash:
    # Set the default profile image as the temporary profile image
    bytes = app_tables.images.get(imageName='userDefault.jpg')['image'].get_bytes()
    userDefault = anvil.BlobMedia(content_type="image/jpg", content=bytes, name='userDefault.jpg')
    newUser.update(profilePicture=userDefault)
    users = app_tables.users.search(tables.order_by("signed_up", ascending=False))
    lastUserID = None
    for user in users:
      lastUserID = user['userID']
      if lastUserID is not None:
        break
    newUserID = "u" + str(int(lastUserID[1:]) + 1)
    if profileName is not None:
      if app_tables.users.get(profileName=profileName):
        return "Duplicated profile name"
      else:
        newUser.update(dubs=0, subscribers=0, userID=newUserID, profileName=profileName, admin=False, subscriptionNewEmailNotification=True, flagNewEmailNotification=True, requestResponseEmailNotification=True)
        return "User is added"
    else:
      # If profile name is not provided
      randomProfileName = 'user'
      randomNumber = 1
      while app_tables.users.get(profileName=randomProfileName):
        randomNumber = randomNumber + 1
        randomProfileName = 'user' + str(randomNumber)
      newUser.update(dubs=0, subscribers=0, userID=newUserID, profileName=randomProfileName, admin=False, subscriptionNewEmailNotification=True, flagNewEmailNotification=True, requestResponseEmailNotification=True)
      return "User is added"
  else:
    return "Wrong password"


@anvil.server.callable
def check_profile_name(profileName):
  """Check whether the profile name existed"""
  user = anvil.users.get_user()
  users = app_tables.users.search(profileName=profileName)
  if len(users) > 1:
    return False
  if len(users) == 1 and user != users[0]:
    return False
  return True


@anvil.server.callable
def stop_continue_subscription_new_dub_email():
  """Stop or continue to receive email notification for new dub from subscribed channel"""
  user = anvil.users.get_user()
  if user['subscriptionNewEmailNotification']:
    user.update(subscriptionNewEmailNotification=False)
    return True
  else:
    user.update(subscriptionNewEmailNotification=True)
    return True


@anvil.server.callable
def get_video_id_from_url(url):
  """Get YT video ID from its URL"""
  if "youtube.com/watch?v=" in url:
    video_id = url.split("v=")[1]
    if ("&" in video_id):
      video_id = video_id.split("&")[0]
    return video_id
  elif ("https://youtu.be/" in url):
    video_id = url.split("https://youtu.be/")[1]
    video_id = video_id.split("?")[0]
    return video_id
  elif ("youtube.com/shorts/" in url):
    video_id = url.split('youtube.com/shorts/')[1]
    if ('?' in video_id):
      video_id = video_id.split('?')[0]
    return video_id
  else:
    # Handle invalid URL
    return None


@anvil.server.callable
def delete_link(linkRow):
  """Delete the link from the link table"""
  if app_tables.links.has_row(linkRow):
    try:
      linkRow.delete()
      return True
    except Exception:
      return False
  else:
    return False


@anvil.server.callable
def delete_audio(audioRow):
  """Delete the dub audio from the audio table"""
  if app_tables.audios.has_row(audioRow):
    try:
      # Also delete the record in the 'liked' table if exists
      relatedLikes = app_tables.likes.search(audioRow=audioRow)
      if len(relatedLikes) > 0:
        for like in relatedLikes:
          like.delete()
      # Also delete the record in the 'disliked' table if exists
      relatedDislikes = app_tables.dislikes.search(audioRow=audioRow)
      if len(relatedDislikes) > 0:
        for dislike in relatedDislikes:
          dislike.delete()
      # Also delete the record in the 'history' table if exists
      relatedHistories = app_tables.histories.search(audioRow=audioRow)
      if len(relatedHistories) > 0:
        for history in relatedHistories:
          history.delete()
      # Also delete the record in the 'flag' table if exists
      relatedFlags = app_tables.flags.search(audioRow=audioRow)
      if len(relatedFlags) > 0:
        for flag in relatedFlags:
          flag.delete()
      # Delete the audio row in the audio table
      audioRow.delete()
      user = anvil.users.get_user()
      # Reduce the number of dub of the channel
      newNumOfDubs = user['dubs'] - 1
      user.update(dubs=newNumOfDubs)
      return True
    except Exception:
      return False
  else:
    return False


@anvil.server.callable
def update_user(user, user_dict):
  """Update user's profile info"""
  if user == anvil.users.get_user():
    try:
      user.update(**user_dict)
      return True
    except Exception:
      return False
  else:
    return False


@anvil.server.callable
def delete_profilePicture(user):
  """Delete / replace the old profile picture with the default picture"""
  if user == anvil.users.get_user():
    bytes = app_tables.images.get(imageName='userDefault.jpg')['image'].get_bytes()
    userDefault = anvil.BlobMedia(content_type="image/jpg", content=bytes, name='userDefault.jpg')
    try:
      user.update(profilePicture=userDefault)
      return True
    except Exception:
      return False
  else:
    return False


@anvil.server.callable
def update_link(linkRow, link_dict):
  """Update the link"""
  if app_tables.links.has_row(linkRow):
    try:
      linkRow.update(**link_dict)
      return True
    except Exception:
      return False
  else:
    return False


@anvil.server.callable
def update_audio(audioRow, audio_dict):
  """Update the date time and other info of the dub"""
  if app_tables.audios.has_row(audioRow):
    audio_dict['createdOn'] = datetime.now()
    try:
      audioRow.update(**audio_dict)
      return True
    except Exception:
      return False
  else:
    return False


@anvil.server.callable
def add_request(request_dict):
  """Add a new dub request"""
  # Prepare for adding a row in the 'requests' table
  user = anvil.users.get_user()
  youTubeVideoID = request_dict['youTubeVideoID']
  videoUrl = 'https://www.youtube.com/watch?v=' + youTubeVideoID
  videoTitle = request_dict['videoTitle']
  requestLanguage = request_dict['language']
  requestAccent = request_dict['accent']
  # Check whether such request already exists in the database
  request = app_tables.requests.get(requestVideoUrl=videoUrl, requestLanguage=requestLanguage, requestAccent=requestAccent, requestedBy=user)
  # If the request does not exist yet
  if request is None:
    # Check whether the 'request' table is empty
    allRequest = app_tables.requests.search(tables.order_by('requestedOn', ascending=False))
    # If empty
    if len(allRequest) == 0:
      try:
        app_tables.requests.add_row(requestID='r1', requestVideoUrl=videoUrl, videoTitle=videoTitle, requestLanguage=requestLanguage, requestAccent=requestAccent, requestedBy=user, requestedOn=datetime.now(), responded=False, checked=False)
        return 'success'
      except Exception:
        return 'fail'
    else:
      try:
        # If not empty
        newRequestID = 'r' + str(int(allRequest[0]['requestID'][1:])+1)
        app_tables.requests.add_row(requestID=newRequestID, requestVideoUrl=videoUrl, videoTitle=videoTitle, requestLanguage=requestLanguage, requestAccent=requestAccent, requestedBy=user, requestedOn=datetime.now(), responded=False, checked=False)
        # Check the total number of request
        allRequest = app_tables.requests.search(tables.order_by('requestedOn', ascending=False))
        # If there are more than 100000 requests
        if len(allRequest) > 100000:
          dateToday = datetime.today()
          dateOneYearAgo = dateToday - timedelta(days=365)
          # Delete the requests that are more than 1 year old
          for row in allRequest:
            if row['requestedOn'].date() < dateOneYearAgo:
              row.delete()
        return 'success'
      except Exception:
        return 'fail'
  else:
    return 'exist'


@anvil.server.callable
def stop_continue_request_response_email():
  """Stop or continue to receive email notification if someone responded to the dub request"""
  user = anvil.users.get_user()
  if user['requestResponseEmailNotification']:
    user.update(requestResponseEmailNotification=False)
    return True
  else:
    user.update(requestResponseEmailNotification=True)
    return True


@anvil.server.callable
def add_link(link_dict):
  """Add a link (of the social media)"""
  user = anvil.users.get_user()
  # Check whether the link existed
  linkRow = app_tables.links.get(socialMediaName=link_dict['socialMediaName'], link=link_dict['link'], user=user)
  if linkRow is None:
    try:
      app_tables.links.add_row(socialMediaName=link_dict['socialMediaName'], link=link_dict['link'], user=user)
      return True
    except Exception:
      return False
  else:
    return False


@anvil.server.callable
def add_audio(audio_dict):
  """Add a new dub audio"""
  user = anvil.users.get_user()
  videoUrl = audio_dict['videoUrl']
  # Get the video title
  youTubeVideoTitle = anvil.server.call('get_video_title_from_url', videoUrl)
  if youTubeVideoTitle is not None:
    # Make sure the video url is in the desired format
    youTubeVideoID = get_video_id_from_url(videoUrl)
    videoUrl = 'https://www.youtube.com/watch?v=' + youTubeVideoID
    # Check whether the video already existed in the database
    video = app_tables.videos.get(videoUrl=videoUrl)
    # Check whether the 'audio' database table is empty
    allAudioRows = app_tables.audios.search()
    if video is None:
      app_tables.videos.add_row(videoTitle=youTubeVideoTitle, videoUrl=videoUrl, youTubeVideoID=youTubeVideoID)
      video = app_tables.videos.get(videoUrl=videoUrl)
    # If 'audio' database table is not empty
    if len(allAudioRows) > 0:
      lastAudioID = str(allAudioRows[len(allAudioRows)-1]['audioID'])
      idNumber = int(lastAudioID[1:]) + 1
      newAudioID = "a" + str(idNumber)
      return add_audio_helper(newAudioID, user, video, audio_dict)
    # If it is empty
    else:
      newAudioID = "a1"
      return add_audio_helper(newAudioID, user, video, audio_dict)
  else:
    return False


def add_audio_helper(newAudioID, user, video, audio_dict):
  """A helper function for the 'add_audio' function"""
  try:
    # Add a row in the audio table
    app_tables.audios.add_row(
      audioID=newAudioID,
      createdOn=datetime.now(),
      likes=0,
      dislikes=0,
      listens=0,
      createdBy=user,
      videoUrl=video,
      language=audio_dict['language'],
      accent=audio_dict['accent'],
      audio=audio_dict['audio'],
      videoTitle=video['videoTitle'],
      blocked=False
    )
    # Increase the number of created dubs of the current user
    user = anvil.users.get_user()
    newNumOfDubs = user['dubs'] + 1
    user.update(dubs=newNumOfDubs)
    # Check whether someone requested for this dub in the past
    requests = app_tables.requests.search(requestVideoUrl=video['videoUrl'], requestLanguage=audio_dict['language'], requestAccent='Any accent')
    # If someone requested before, change the 'responded' attribute of the requests to True and notify the requesters by email if they allow email notification
    if len(requests) > 0:
      for request in requests:
        if request['requestedBy']['requestResponseEmailNotification']:
          request.update(responded=True)
          emailText = 'Someone responded to your dub request for the video: [' + request['videoTitle'] + '] in the language: [' + request['requestLanguage'] + '] and accent: [' + request['requestAccent'] + ']!'
          emailText += '<br/><br/>Check it out now!: '
          url = 'https://dubtube.anvil.app/#video?ytid=' + video['youTubeVideoID'] + '&audioid=' + newAudioID
          html = emailText + '<a href="' + url + '">' + url + '</a>'
          anvil.email.send(from_name = "DubTubeNotification", 
                    to = request['requestedBy']['email'],
                    subject = "[DubTube] Someone responded to your dub request!",
                    html = html)
    # Check whether someone requested for this dub in this language and accent in the past
    requests = app_tables.requests.search(requestVideoUrl=video['videoUrl'], requestLanguage=audio_dict['language'], requestAccent=audio_dict['accent'])
    # If someone requested before, change the 'responded' attribute of the requests to True and notify the requesters by email if they allow email notification
    if len(requests) > 0:
      for request in requests:
        if request['requestedBy']['requestResponseEmailNotification']:
          request.update(responded=True)
          emailText = 'Someone responded to your dub request for the video: [' + request['videoTitle'] + '] in the language: [' + request['requestLanguage'] + '] and accent: [' + request['requestAccent'] + ']!'
          emailText += '<br/><br/>Check it out now!: '
          url = 'https://dubtube.anvil.app/#video?ytid=' + video['youTubeVideoID'] + '&audioid=' + newAudioID
          html = emailText + '<a href="' + url + '">' + url + '</a>'
          anvil.email.send(from_name = "DubTubeNotification", 
                    to = request['requestedBy']['email'],
                    subject = "[DubTube] Someone responded to your dub request!",
                    html = html)
    # Check whether anyone subscribed to the current user
    subscribers = app_tables.subscriptions.search(userID=user)
    # If the current user has subscribers, email the subscribers about the new dub if they allow email notification
    if len(subscribers) > 0:
      for subscriber in subscribers:
        if subscriber['subscribedBy']['subscriptionNewEmailNotification']:
          emailText = 'The channel you subscribed to: [' + user['profileName'] + '] created a new dub for the video: [' + video['videoTitle'] + '] in the language: [' + audio_dict['language'] + '] and accent: [' + audio_dict['accent'] + ']!'
          emailText += '<br/><br/>Check it out now!: '
          url = 'https://dubtube.anvil.app/#video?ytid=' + video['youTubeVideoID'] + '&audioid=' + newAudioID
          html = emailText + '<a href="' + url + '">' + url + '</a>'
          anvil.email.send(from_name = "DubTubeNotification", 
                    to = subscriber['subscribedBy']['email'],
                    subject = "[DubTube] " + user['profileName'] + " created a new dub",
                    html = html)
    return True
  except Exception:
    return False


@anvil.server.callable
def get_dubs(language='Any language', accent='Any accent', numberOfResults=5, user=None, date=datetime.now().date()):
  """Get the specified dub from the database"""
  if user is None:
    return get_dubs_helper(language, accent, numberOfResults)
  else:
    listOfDubs = get_dubs_with_user_helper(language, accent, user)
    if date == datetime.now().date():
      return listOfDubs
    else:
      limitedListOfDubs = []
      for dub in listOfDubs[0]:
        if dub['createdOn'].date() <= date:
          limitedListOfDubs.append(dub)
      return [limitedListOfDubs, listOfDubs[1]]
      

@anvil.server.callable
def get_dubs_helper(language, accent, numberOfResults):
  """Helper function for the 'get_dubs' function"""
  dubRows = []
  if language=='Any language' and accent=='Any accent':
    dubRows = app_tables.audios.search(tables.order_by("listens", ascending=False))
  elif language!='Any language' and accent=='Any accent':
    dubRows = app_tables.audios.search(tables.order_by("listens", ascending=False), language=language)
  elif language=='Any language' and accent!='Any accent':
    dubRows = app_tables.audios.search(tables.order_by("listens", ascending=False), accent=accent)
  else:
    dubRows = app_tables.audios.search(tables.order_by("listens", ascending=False), language=language, accent=accent)
  if len(dubRows) > numberOfResults:
    limitedDubRows = []
    for i in range(numberOfResults):
      limitedDubRows.append(dubRows[i])
    return limitedDubRows
  else:
    return dubRows


@anvil.server.callable
def get_dubs_with_user_helper(language, accent, user):
  """Helper function with 'user' as parameter for the 'get_dubs' function"""
  atLeastOneDub = False
  dubRows = app_tables.audios.search(tables.order_by("createdOn", ascending=False), createdBy=user)
  if len(dubRows) != 0:
    atLeastOneDub = True
  else:
    return [[], atLeastOneDub]
  if language=='Any language' and accent=='Any accent':
    return [dubRows, atLeastOneDub]
  elif language!='Any language' and accent=='Any accent':
    dubRows = app_tables.audios.search(tables.order_by("createdOn", ascending=False), language=language, createdBy=user)
    return [dubRows, atLeastOneDub]
  elif language=='Any language' and accent!='Any accent':
    dubRows = app_tables.audios.search(tables.order_by("createdOn", ascending=False), accent=accent, createdBy=user)
    return [dubRows, atLeastOneDub]
  else:
    dubRows = app_tables.audios.search(tables.order_by("createdOn", ascending=False), language=language, accent=accent, createdBy=user)
    return [dubRows, atLeastOneDub]


@anvil.server.callable
def get_requests(language='Any language', accent='Any accent', numberOfResults=5, user=None, date=datetime.now().date()):
  """Get the request from the database"""
  if user is None:
    listOfRequests = get_requests_helper(language, accent, numberOfResults)
  else:
    currentUser = anvil.users.get_user()
    if currentUser == user:
      listOfRequests = get_requests_with_user_helper(language, accent, currentUser)
      if date == datetime.now().date():
        return listOfRequests        
    else:
      return [[], []]
  limitedListOfRequests = []
  limitedNumberOfRequestList = []
  requestRows = listOfRequests[0]
  numberOfRequestList = listOfRequests[1]
  # Zip and sort based on the second list in descending order
  zipped_sorted = sorted(zip(requestRows, numberOfRequestList), key=lambda x: x[1], reverse=True)
  requestRows, numberOfRequestList = zip(*zipped_sorted)
  for i in range(len(requestRows)):
    if requestRows[i]['requestedOn'].date() <= date:
      limitedListOfRequests.append(requestRows[i])
      limitedNumberOfRequestList.append(numberOfRequestList[i])
  return [limitedListOfRequests, limitedNumberOfRequestList]


@anvil.server.callable
def get_requests_helper(language, accent, numberOfResults):
  """Helper function for the 'get_requests' function"""
  requestRows = []
  # numberOfRequestList = []
  if language=='Any language' and accent=='Any accent':
    requestRows = app_tables.requests.search(tables.order_by("requestedOn", ascending=True))
  elif language!='Any language' and accent=='Any accent':
    requestRows = app_tables.requests.search(tables.order_by("requestedOn", ascending=True), requestLanguage=language)
  elif language=='Any language' and accent!='Any accent':
    requestRows = app_tables.requests.search(tables.order_by("requestedOn", ascending=True), requestAccent=accent)
  else:
    requestRows = app_tables.requests.search(tables.order_by("requestedOn", ascending=True), requestLanguage=language, requestAccent=accent)
  if len(requestRows) > numberOfResults:
    limitedRequestRows = []
    for i in range(numberOfResults):
      limitedRequestRows.append(requestRows[i])
    requestRows = limitedRequestRows
  pureRequestRows = [[requestRow['requestVideoUrl'], requestRow['videoTitle'], requestRow['requestLanguage'], requestRow['requestAccent']] for requestRow in requestRows]
  # Count the repetition of the requests
  # Convert inner lists to tuples to make them hashable
  hashablePureRequestRows = [tuple(inner_list) for inner_list in pureRequestRows]
  element_counts = Counter(hashablePureRequestRows)
  uniqueRequestRows = list(element_counts.keys())
  requestRepetition = list(element_counts.values())
  returnRequestRows = []
  for uniqueRequest in uniqueRequestRows:
    for request in requestRows:
      if request['requestVideoUrl']==uniqueRequest[0] and request['requestLanguage']==uniqueRequest[2] and request['requestAccent']==uniqueRequest[3]:
        returnRequestRows.append(request)
        break
  return [returnRequestRows, requestRepetition]


@anvil.server.callable
def get_requests_with_user_helper(language, accent, user):
  """Helper function of the 'get_requests' function with the current user as a parameter"""
  requestRows = app_tables.requests.search(tables.order_by("requestedOn", ascending=False), requestedBy=user)
  if len(requestRows) == 0:
    return [[], []]
  else:
    if language=='Any language' and accent=='Any accent':
      pass
    elif language!='Any language' and accent=='Any accent':
      requestRows = app_tables.requests.search(tables.order_by("requestedOn", ascending=False), requestLanguage=language, requestedBy=user)
    elif language=='Any language' and accent!='Any accent':
      requestRows = app_tables.requests.search(tables.order_by("requestedOn", ascending=False), requestAccent=accent, requestedBy=user)
    else:
      requestRows = app_tables.requests.search(tables.order_by("requestedOn", ascending=False), requestLanguage=language, requestAccent=accent, requestedBy=user)
    numberOfRequestsList = []
    for request in requestRows:
      numberOfRequests = len(app_tables.requests.search(requestVideoUrl=request['requestVideoUrl'], requestLanguage=request['requestLanguage'], requestAccent=request['requestAccent']))
      numberOfRequestsList.append(numberOfRequests)
    return [requestRows, numberOfRequestsList]


@anvil.server.callable
def get_links(user=None):
  """Get the links"""
  if user is None:
    user = anvil.users.get_user()
  return app_tables.links.search(user=user)


@anvil.server.callable
def get_subscriptions():
  """Get the subscriptions"""
  user = anvil.users.get_user()
  subscriptions = app_tables.subscriptions.search(tables.order_by('subscribedOn', ascending=False), subscribedBy=user)
  newReleaseNotListenedList = []
  # If the current user subscribed to some channels
  if len(subscriptions) > 0:
    newReleaseNotListened = False
    for subscription in subscriptions:
      # Get the dubs of the channels
      dubs = app_tables.audios.search(tables.order_by('createdOn', ascending=False), createdBy=subscription['userID'])
      if len(dubs) > 0:
        latestDub = dubs[0]
        latestDubDate = latestDub['createdOn'].date()
        date3DaysAgo = (datetime.today() - timedelta(days=3)).date()
        if latestDubDate >= date3DaysAgo:
          newReleaseNotListened = True
          # Check whether the user has listened to the new released dubs
          histories = app_tables.histories.search(tables.order_by('listenedOn', ascending=False), listenedBy=user)
          for history in histories:
            if history['audioRow'] == latestDub:
              newReleaseNotListened = False
              break
            if history['listenedOn'].date() < date3DaysAgo:
              break
      newReleaseNotListenedList.append(newReleaseNotListened)
  return [subscriptions, newReleaseNotListenedList]


@anvil.server.callable
def new_released_not_listened():
  """Check whether there are newly released dubs that are not yet listened by the subscribers"""
  user = anvil.users.get_user()
  subscriptions = app_tables.subscriptions.search(tables.order_by('subscribedOn', ascending=False), subscribedBy=user)
  if len(subscriptions) > 0:
    newReleaseNotListened = False
    for subscription in subscriptions:
      dubs = app_tables.audios.search(tables.order_by('createdOn', ascending=False), createdBy=subscription['userID'])
      if len(dubs) > 0:
        latestDub = dubs[0]
        latestDubDate = latestDub['createdOn'].date()
        date3DaysAgo = (datetime.today() - timedelta(days=3)).date()
        if latestDubDate >= date3DaysAgo:
          newReleaseNotListened = True
          histories = app_tables.histories.search(tables.order_by('listenedOn', ascending=False), listenedBy=user)
          for history in histories:
            if history['audioRow'] == latestDub:
              newReleaseNotListened = False
              break
            if history['listenedOn'].date() < date3DaysAgo:
              break
      if newReleaseNotListened:
        return True
  return False


@anvil.server.callable
def get_search_requests(videoUrl, videotitlekeyword, user=None):
  """Get the searched requests"""
  if videoUrl != '' and videotitlekeyword == '':
    videoUrl = 'https://www.youtube.com/watch?v=' + get_video_id_from_url(videoUrl)
    if user is None:
      requestRows = app_tables.requests.search(tables.order_by('requestedOn', ascending=False), requestVideoUrl=videoUrl)
    else:
      requestRows = app_tables.requests.search(tables.order_by('requestedOn', ascending=False), requestVideoUrl=videoUrl, requestedBy=user)
    numberOfRequestList = []
    for request in requestRows:
      numberOfRequest = len(app_tables.requests.search(requestVideoUrl=request['requestVideoUrl'], requestLanguage=request['requestLanguage'], requestAccent=request['requestAccent']))
      numberOfRequestList.append(numberOfRequest)
    return [requestRows, numberOfRequestList]
  elif videoUrl == '' and videotitlekeyword != '':
    keywords = videotitlekeyword.split(' ')
    # Change the keywords to lower case
    smallKeywords = [keyword.lower() for keyword in keywords]
    if user is None:
      requestRows = app_tables.requests.search(tables.order_by('requestedOn', ascending=False))
    else:
      requestRows = app_tables.requests.search(tables.order_by('requestedOn', ascending=False), requestedBy=user)
    videoTitles = [request['videoTitle'] for request in requestRows]
    # Created a list of an ordered dictionary
    videoTitles = list(OrderedDict.fromkeys(videoTitles))
    # Change the titles to lower case to match the keywords
    smallVideoTitles = [request['videoTitle'].lower() for request in requestRows]
    smallVideoTitles = list(OrderedDict.fromkeys(smallVideoTitles))
    numberOfMatchList = []
    for smallVideoTitle in smallVideoTitles:
      numberOfMatch = 0
      for keyword in smallKeywords:
        if keyword in smallVideoTitle:
          numberOfMatch += 1
      numberOfMatchList.append(numberOfMatch)
    zipped_list = [(s, i) for s, i in zip(videoTitles, numberOfMatchList) if i != 0]
    # Sort based on the number of matches
    sorted_list = sorted(zipped_list, key=lambda x: x[1], reverse=True)
    sortedVideoTitles = [pair[0] for pair in sorted_list]
    if len(sortedVideoTitles) == 0:
      return [[], []]
    else:
      requestRows = []
      numberOfRequestList = []
      for videoTitle in sortedVideoTitles:
        if user is None:
          requestRows.extend(app_tables.requests.search(tables.order_by('requestedOn', ascending=False), videoTitle=videoTitle))
        else:
          requestRows.extend(app_tables.requests.search(tables.order_by('requestedOn', ascending=False), videoTitle=videoTitle, requestedBy=user))
      for request in requestRows:
        numberOfRequest = len(app_tables.requests.search(requestVideoUrl=request['requestVideoUrl'], requestLanguage=request['requestLanguage'], requestAccent=request['requestAccent']))
        numberOfRequestList.append(numberOfRequest)
      return [requestRows, numberOfRequestList]

      
@anvil.server.callable
def get_search_dubs(videoUrl, videotitlekeyword, language='Any language', accent='Any accent'):
  """Get the searched dubs"""
  if videoUrl != '' and videotitlekeyword == '':
    videoUrl = 'https://www.youtube.com/watch?v=' + get_video_id_from_url(videoUrl)
    videoRow = app_tables.videos.get(videoUrl=videoUrl)
    if videoRow is not None:
      if language=='Any language' and accent=='Any accent':
        dubRows = app_tables.audios.search(tables.order_by("listens", ascending=False), videoUrl=videoRow)
        return [dubRows, True]
      elif language!='Any language' and accent=='Any accent':
        dubRows = app_tables.audios.search(tables.order_by("listens", ascending=False), language=language, videoUrl=videoRow)
        return [dubRows, True]
      elif language=='Any language' and accent!='Any accent':
        dubRows = app_tables.audios.search(tables.order_by("listens", ascending=False), accent=accent, videoUrl=videoRow)
        return [dubRows, True]
      else:
        dubRows = app_tables.audios.search(tables.order_by("listens", ascending=False), language=language, accent=accent, videoUrl=videoRow)
        return [dubRows, True]
    else:
      return [[], False]
  elif videoUrl == '' and videotitlekeyword != '':
    keywords = videotitlekeyword.split(' ')
    smallKeywords = [keyword.lower() for keyword in keywords]
    videoRows = app_tables.videos.search()
    videoTitles = [videoRow['videoTitle'] for videoRow in videoRows]
    smallVideoTitles = [videoRow['videoTitle'].lower() for videoRow in videoRows]
    numberOfMatchList = []
    for smallVideoTitle in smallVideoTitles:
      numberOfMatch = 0
      for keyword in smallKeywords:
        if keyword in smallVideoTitle:
          numberOfMatch += 1
      numberOfMatchList.append(numberOfMatch)
    zipped_list = [(s, i) for s, i in zip(videoTitles, numberOfMatchList) if i != 0]
    sorted_list = sorted(zipped_list, key=lambda x: x[1], reverse=True)
    sortedVideoTitles = [pair[0] for pair in sorted_list]
    if len(sortedVideoTitles) == 0:
      # no match videos
      return [[], False]
    else:
      audioRows = []
      if language=='Any language' and accent=='Any accent':
        for videoTitle in sortedVideoTitles:
          audioRows.extend(app_tables.audios.search(tables.order_by('likes', ascending=False), videoTitle=videoTitle))
        return [audioRows, True]
      elif language!='Any language' and accent=='Any accent':
        for videoTitle in sortedVideoTitles:
          audioRows.extend(app_tables.audios.search(tables.order_by('likes', ascending=False), videoTitle=videoTitle, language=language))
        return [audioRows, True]
      elif language=='Any language' and accent!='Any accent':
        for videoTitle in sortedVideoTitles:
          audioRows.extend(app_tables.audios.search(tables.order_by('likes', ascending=False), videoTitle=videoTitle, accent=accent))
        return [audioRows, True]
      else:
        for videoTitle in sortedVideoTitles:
          audioRows.extend(app_tables.audios.search(tables.order_by('likes', ascending=False), videoTitle=videoTitle, language=language, accent=accent))
        return [audioRows, True]


@anvil.server.callable
def get_video(url):
  """Get the video row from the 'video' table based on the url"""
  if get_video_id_from_url(url) is not None:
    return app_tables.videos.get(videoUrl=url)
  else:
    return None


@anvil.server.callable
def get_video_player_dubs(videoUrl, language='Any language', accent='Any accent'):
  """Get the dubs for the video player page based on the video url, the language, and the accent"""
  if language=='Any language' and accent=='Any accent':
    return app_tables.audios.search(tables.order_by("listens", ascending=False), videoUrl=videoUrl)
  elif language!='Any language' and accent=='Any accent':
    return app_tables.audios.search(tables.order_by("listens", ascending=False), videoUrl=videoUrl, language=language)
  elif language=='Any language' and accent!='Any accent':
    return app_tables.audios.search(tables.order_by("listens", ascending=False), videoUrl=videoUrl, accent=accent)
  else:
    return app_tables.audios.search(tables.order_by("listens", ascending=False), videoUrl=videoUrl, language=language, accent=accent)


@anvil.server.callable
def get_first_audio(videoUrl):
  """Get the first dub that appeared in the data base table for the specific video"""
  return app_tables.audios.search(videoUrl=videoUrl)[0]['audio']


@anvil.server.callable
def subscribeUnsubscribe(channelOwner):
  """Subscribe or unsubscribe to the channel"""
  currentUser = anvil.users.get_user()
  subscription = app_tables.subscriptions.get(userID=channelOwner, subscribedBy=currentUser)
  # Subscribe if not subscribed yet
  if subscription is None:
    try:
      app_tables.subscriptions.add_row(userID=channelOwner, subscribedBy=currentUser, subscribedOn=datetime.now())
      newNumOfSubscribers = channelOwner['subscribers'] + 1
      channelOwner.update(subscribers=newNumOfSubscribers)
      return True
    except Exception:
      return False
  else:
    # Unsubscribe if subscribed
    try:
      subscription.delete()
      newNumOfSubscribers = channelOwner['subscribers'] - 1
      channelOwner.update(subscribers=newNumOfSubscribers)
      return True
    except Exception:
      return False


@anvil.server.callable
def checkSubscription(channelOwner):
  """Check whether the current user subscribed to the given channel"""
  currentUser = anvil.users.get_user()
  subscription = app_tables.subscriptions.get(userID=channelOwner, subscribedBy=currentUser)
  if subscription is None:
    return False
  else:
    return True


@anvil.server.callable
def get_flag(audioRow):
  """Get the flag raised by the current user about the given dub"""
  user = anvil.users.get_user()
  return app_tables.flags.get(audioRow=audioRow, flaggedBy=user)


@anvil.server.callable
def get_flags_admin():
  """Get all the flags for admin"""
  user = anvil.users.get_user()
  if user['admin'] is False:
    anvil.users.logout()
  else:
    receivedFlags = app_tables.flags.search(tables.order_by('flaggedOn', ascending=True))
    uniqueFlaggedAudio = []
    uniqueReason = []
    repetition = []
    flagDetailsList = []
    flagFirstDateList = []
    readList = []
    if len(receivedFlags) > 0:
      flaggedAudioAndReason = [[flag['audioRow'], flag['flagReason']] for flag in receivedFlags]
      hashableFlaggedAudioAndReason = [tuple(inner_list) for inner_list in flaggedAudioAndReason]
      # Count the number of unique flagged audio + reason
      element_counts = Counter(hashableFlaggedAudioAndReason)
      uniqueFlaggedAudioAndReason = list(element_counts.keys())
      repetition = list(element_counts.values())
      uniqueFlaggedAudio = [x[0] for x in uniqueFlaggedAudioAndReason]
      uniqueReason = [x[1] for x in uniqueFlaggedAudioAndReason]
      # Get the date when the audio was first flagged for this specific reason
      for item in uniqueFlaggedAudioAndReason:
        flagDetails = set()
        flagFirstDate = ''
        read = True
        for flag in receivedFlags:
          if flag['audioRow'] == item[0] and flag['flagReason'] == item[1]:
            flagDetails.add(flag['flagDetails'])
            if flagFirstDate == '':
              flagFirstDate = flag['flaggedOn']
            if flag['readAdmin'] is False:
              read = False
        flagDetailsList.append(list(flagDetails))
        flagFirstDateList.append(flagFirstDate)
        readList.append(read)
    return list(zip(uniqueFlaggedAudio, uniqueReason, repetition, flagFirstDateList, flagDetailsList, readList))


@anvil.server.callable
def get_flags():
  """Get all the flags for the admin"""
  user = anvil.users.get_user()
  if user['admin']:
    receivedFlags = app_tables.flags.search(tables.order_by('flaggedOn', ascending=True))
    uniqueFlaggedAudio = []
    uniqueReason = []
    repetition = []
    flagDetailsList = []
    flagFirstDateList = []
    if len(receivedFlags) > 0:
      flaggedAudioAndReason = [[flag['audioRow'], flag['flagReason']] for flag in receivedFlags]
      hashableFlaggedAudioAndReason = [tuple(inner_list) for inner_list in flaggedAudioAndReason]
      element_counts = Counter(hashableFlaggedAudioAndReason)
      uniqueFlaggedAudioAndReason = list(element_counts.keys())
      repetition = list(element_counts.values())
      uniqueFlaggedAudio = [x[0] for x in uniqueFlaggedAudioAndReason]
      uniqueReason = [x[1] for x in uniqueFlaggedAudioAndReason]
      for item in uniqueFlaggedAudioAndReason:
        flagDetails = set()
        flagFirstDate = ''
        for flag in receivedFlags:
          if flag['audioRow'] == item[0] and flag['flagReason'] == item[1]:
            flagDetails.add(flag['flagDetails'])
            if flagFirstDate == '':
              flagFirstDate = flag['flaggedOn']
        flagDetailsList.append(list(flagDetails))
        flagFirstDateList.append(flagFirstDate)
    return list(zip(uniqueFlaggedAudio, uniqueReason, repetition, flagFirstDateList, flagDetailsList))


@anvil.server.callable
def delete_flags_admin(audioRow, flagReason):
  """Delete the flags (Admin's function)"""
  user = anvil.users.get_user()
  if user['admin']:
    flags = app_tables.flags.search(audioRow=audioRow, flagReason=flagReason)
    if len(flags) > 0:
      for flag in flags:
        flag.delete()
      return True
    else:
      return False
  else:
    return None


@anvil.server.callable
def get_my_flags():
  """Get the flags raised by the current user"""
  user = anvil.users.get_user()
  return app_tables.flags.search(tables.order_by('flaggedOn', ascending=False), flaggedBy=user)


@anvil.server.callable
def unread_flags():
  """Check if there are received flags that have not been viewed by the current user"""
  user = anvil.users.get_user()
  receivedFlags = app_tables.flags.search(read=False)
  for flag in receivedFlags:
    if flag['audioRow']['createdBy'] == user:
      return True
  return False


@anvil.server.callable
def get_my_received_flags():
  """Get the flags received by the current user"""
  user = anvil.users.get_user()
  allFlags = app_tables.flags.search(tables.order_by('flaggedOn', ascending=True))
  receivedFlags = []
  uniqueFlaggedAudio = []
  uniqueReason = []
  repetition = []
  flagDetailsList = []
  flagFirstDateList = []
  readList = []
  if len(allFlags) > 0:
    for flag in allFlags:
      if flag['audioRow']['createdBy'] == user:
        receivedFlags.append(flag)
    if len(receivedFlags) > 0:
      flaggedAudioAndReason = [[flag['audioRow'], flag['flagReason']] for flag in receivedFlags]
      hashableFlaggedAudioAndReason = [tuple(inner_list) for inner_list in flaggedAudioAndReason]
      # Count the number of repetition for the received flags with the same reason
      element_counts = Counter(hashableFlaggedAudioAndReason)
      uniqueFlaggedAudioAndReason = list(element_counts.keys())
      repetition = list(element_counts.values())
      uniqueFlaggedAudio = [x[0] for x in uniqueFlaggedAudioAndReason]
      uniqueReason = [x[1] for x in uniqueFlaggedAudioAndReason]
      # Get the date when the dub is flagged for the first time
      for item in uniqueFlaggedAudioAndReason:
        flagDetails = set()
        flagFirstDate = ''
        read = True
        for flag in receivedFlags:
          if flag['audioRow'] == item[0] and flag['flagReason'] == item[1]:
            flagDetails.add(flag['flagDetails'])
            if flagFirstDate == '':
              flagFirstDate = flag['flaggedOn']
            if flag['read'] is False:
              read = False
        flagDetailsList.append(list(flagDetails))
        flagFirstDateList.append(flagFirstDate)
        readList.append(read)
  return list(zip(uniqueFlaggedAudio, uniqueReason, repetition, flagFirstDateList, flagDetailsList, readList))


@anvil.server.callable
def mark_flag_read(audioRow, reason):
  """Mark the flag as viewed by the channel"""
  flags = app_tables.flags.search(audioRow=audioRow, flagReason=reason)
  for flag in flags:
    flag.update(read=True)
    

@anvil.server.callable
def mark_flag_read_admin(audioRow, reason):
  """Mark the flag as viewed by the admin"""
  flags = app_tables.flags.search(audioRow=audioRow, flagReason=reason)
  for flag in flags:
    flag.update(readAdmin=True)


@anvil.server.callable
def delete_flag(audioRow):
  """Delete the flag"""
  user = anvil.users.get_user()
  flag = app_tables.flags.get(audioRow=audioRow, flaggedBy=user)
  if flag is not None:
    try:
      flag.delete()
      return True
    except Exception:
      return False
  else:
    return False


@anvil.server.callable
def flag_dub(audioRow, flag_dict):
  """Flag a dub"""
  user = anvil.users.get_user()
  flag = app_tables.flags.get(audioRow=audioRow, flaggedBy=user)
  if flag is None:
    try:
      # Send an email to the channel owner
      app_tables.flags.add_row(audioRow=audioRow, flagReason=flag_dict['flagReason'], flagDetails=flag_dict['flagDetails'], flaggedBy=user, flaggedOn=datetime.now(), read=False, readAdmin=False)
      if audioRow['createdBy']['flagNewEmailNotification']:
        emailText = "Someone flagged your dub for the video: [" + audioRow['videoTitle'] + "] in the language: [" + audioRow['language'] + "] and accent: [" + audioRow['accent'] + "] with the reason: [" + flag_dict['flagReason'] + "] and details: [" + flag_dict['flagDetails'] + "].\n"
        emailText += "If necessary, please edit your dub accordingly as soon as possible. Thank you."
        anvil.email.send(from_name = "DubTubeNotification", 
                  to = audioRow['createdBy']['email'],
                  subject = "[DubTube] Your dub has been flagged by someone",
                  text = emailText)
      return True
    except Exception:
      return False
  else:
    try:
      flag.update(flagReason=flag_dict['flagReason'], flagDetails=flag_dict['flagDetails'], flaggedOn=datetime.now(), read=False, readAdmin=False)
      return True
    except Exception:
      return False


@anvil.server.callable
def stop_continue_flag_email():
  """Stop or continue to receive email notification about dubs getting flagged"""
  user = anvil.users.get_user()
  if user['flagNewEmailNotification']:
    user.update(flagNewEmailNotification=False)
    return True
  else:
    user.update(flagNewEmailNotification=True)
    return True


@anvil.server.callable
def like_dub(audioRow):
  """Like a dub and remove it from the disliked table if it was there"""
  user = anvil.users.get_user()
  liked = app_tables.likes.get(audioRow=audioRow, likedBy=user)
  if liked is None:
    newLike = audioRow['likes'] + 1
    audioRow.update(likes=newLike)
    app_tables.likes.add_row(audioRow=audioRow, likedBy=user, likedOn=datetime.now())
    disliked = app_tables.dislikes.get(audioRow=audioRow, dislikedBy=user)
    if disliked is not None:
      disliked.delete()
      newDislike = audioRow['dislikes'] - 1
      audioRow.update(dislikes=newDislike)
  else:
    newLike = audioRow['likes'] - 1
    audioRow.update(likes=newLike)
    liked.delete()


@anvil.server.callable
def dislike_dub(audioRow):
  """Dislike a dub and remove it from the liked table if it was there"""
  user = anvil.users.get_user()
  disliked = app_tables.dislikes.get(audioRow=audioRow, dislikedBy=user)
  if disliked is None:
    newDislike = audioRow['dislikes'] + 1
    audioRow.update(dislikes=newDislike)
    app_tables.dislikes.add_row(audioRow=audioRow, dislikedBy=user, dislikedOn=datetime.now())
    liked = app_tables.likes.get(audioRow=audioRow, likedBy=user)
    if liked is not None:
      liked.delete()
      newLike = audioRow['likes'] - 1
      audioRow.update(likes=newLike)
  else:
    newDislike = audioRow['dislikes'] - 1
    audioRow.update(dislikes=newDislike)
    disliked.delete()


@anvil.server.callable
def userPastPreference(audioRow):
  """Check whether the user liked, disliked, flagged the dub before"""
  user = anvil.users.get_user()
  likesRow = app_tables.likes.get(audioRow=audioRow, likedBy=user)
  dislikesRow = app_tables.dislikes.get(audioRow=audioRow, dislikedBy=user)
  flagsRow = app_tables.flags.get(audioRow=audioRow, flaggedBy=user)
  likeDislikeFlag = [False, False, False]
  if likesRow is not None:
    likeDislikeFlag[0] = True
  if dislikesRow is not None:
    likeDislikeFlag[1] = True
  if flagsRow is not None:
    likeDislikeFlag[2] = True
  return likeDislikeFlag


@anvil.server.callable
def listen_dub(audioID):
  """Add the listened dub to the history table and update the number of listens"""
  audioRow = app_tables.audios.get(audioID=audioID)
  if audioRow is not None:
    newListens = audioRow['listens'] + 1
    audioRow.update(listens=newListens)
    user = anvil.users.get_user()
    if user is not None:
      listened = app_tables.histories.get(audioRow=audioRow, listenedBy=user)
      if listened is not None:
        listened.update(listenedOn=datetime.now())
      else:
        app_tables.histories.add_row(audioRow=audioRow, listenedBy=user, listenedOn=datetime.now())
      listOfListened = app_tables.histories.search(listenedBy=user)
      # Delete listen history if there are more than 100 records
      if len(listOfListened) > 100:
        dateToday = datetime.today()
        date60DaysAgo = dateToday - timedelta(days=60)
        for row in listOfListened:
          if row['listenedOn'].date() < date60DaysAgo:
            row.delete()


@anvil.server.callable
def get_histories(date=datetime.now().date(), language='Any language', accent='Any accent'):
  """Get the listen history of the current user"""
  user = anvil.users.get_user()
  if user is not None:
    listOfHistories = app_tables.histories.search(tables.order_by('listenedOn', ascending=False), listenedBy=user)
    # Check whether the dubs in the history database are published dubs
    for history in listOfHistories:
      try:
        # Published dubs should have at least 2 characters as ID
        if len(history['audioRow']['audioID']) >= 2:
          pass
      except Exception:
        history.delete()
    listOfHistories = app_tables.histories.search(tables.order_by('listenedOn', ascending=False), listenedBy=user)
    if date == datetime.now().date():
      audioRows = [history['audioRow'] for history in listOfHistories]
      listenedOns = [history['listenedOn'].date() for history in listOfHistories]
      return get_histories_helper(audioRows, listenedOns, language, accent)
    else:
      audioRows = []
      listenedOns = []
      for history in listOfHistories:
        if history['listenedOn'].date() <= date:
          audioRows.append(history['audioRow'])
          listenedOns.append(history['listenedOn'].date())
      return get_histories_helper(audioRows, listenedOns, language, accent)
  else:
    return None


@anvil.server.callable
def get_histories_helper(audioRows, listenedOns, language, accent):
  """Helper function for the 'get_histories' function to filter the histories based on the language, accent"""
  user = anvil.users.get_user()
  if language == 'Any language' and accent == 'Any accent':
    return [audioRows, listenedOns]
  elif language == 'Any language' and accent != 'Any accent':
    accentAudioRows = []
    listenedOns = []
    for audioRow in audioRows:
      if audioRow['accent'] == accent:
        accentAudioRows.append(audioRow)
        listenedOns.append(app_tables.histories.get(audioRow=audioRow, listenedBy=user)['listenedOn'].date())
    return [accentAudioRows, listenedOns]
  elif language != 'Any language' and accent == 'Any accent':
    languageAudioRows = []
    listenedOns = []
    for audioRow in audioRows:
      if audioRow['language'] == language:
        languageAudioRows.append(audioRow)
        listenedOns.append(app_tables.histories.get(audioRow=audioRow, listenedBy=user)['listenedOn'].date())
    return [languageAudioRows, listenedOns]
  else:
    languageAccentAudioRows = []
    listenedOns = []
    for audioRow in audioRows:
      if audioRow['language'] == language and audioRow['accent'] == accent:
        languageAudioRows.append(audioRow)
        listenedOns.append(app_tables.histories.get(audioRow=audioRow, listenedBy=user)['listenedOn'].date())
    return [languageAccentAudioRows, listenedOns]


@anvil.server.callable
def delete_history(audioRow):
  """Delete history based on the dub and the current user"""
  user = anvil.users.get_user()
  if user is not None:
    listened = app_tables.histories.get(audioRow=audioRow, listenedBy=user)
    if listened is not None:
      listened.delete()


@anvil.server.callable
def delete_request(request):
  """Delete request"""
  user = anvil.users.get_user()
  if user is not None and app_tables.requests.has_row(request):
    request.delete()


@anvil.server.callable
def clear_history():
  user = anvil.users.get_user()
  if user is not None:
    listOfListened = app_tables.histories.search(listenedBy=user)
    for listened in listOfListened:
      listened.delete()

@anvil.server.callable
def clear_request():
  """Clear requests"""
  user = anvil.users.get_user()
  if user is not None:
    requests = app_tables.requests.search(requestedBy=user)
    for request in requests:
      request.delete()


@anvil.server.callable
def get_liked(date=datetime.now().date(), language='Any language', accent='Any accent'):
  user = anvil.users.get_user()
  if user is not None:
    listOfLiked = app_tables.likes.search(likedBy=user)
    # Make sure only published dub can be liked
    for likeRow in listOfLiked:
      try:
        # The audio ID of published dubs have at least 2 characters
        if len(likeRow['audioRow']['audioID']) >= 2:
          pass
      except Exception:
        likeRow.delete()
    listOfLiked = app_tables.likes.search(tables.order_by('likedOn', ascending=False), likedBy=user)
    listOfDisliked = app_tables.dislikes.search(dislikedBy=user)
    # Make sure only published dub can be disliked
    for dislikeRow in listOfDisliked:
      try:
        # The audio ID of published dubs have at least 2 characters
        if len(dislikeRow['audioRow']['audioID']) >= 2:
          pass
      except Exception:
        dislikeRow.delete()
    if date == datetime.now().date():
      audioRows = [liked['audioRow'] for liked in listOfLiked]
      likedOns = [liked['likedOn'].date() for liked in listOfLiked]
      return get_liked_helper(audioRows, likedOns, language, accent)
    else:
      audioRows = []
      likedOns = []
      for liked in listOfLiked:
        if liked['likedOn'].date() <= date:
          audioRows.append(liked['audioRow'])
          likedOns.append(liked['likedOn'].date())
      return get_liked_helper(audioRows, likedOns, language, accent)
  else:
    return None


@anvil.server.callable
def get_liked_helper(audioRows, likedOns, language, accent):
  """Helper function of the 'get_liked' function to filter the results by language and accent"""
  user = anvil.users.get_user()
  if language == 'Any language' and accent == 'Any accent':
    return [audioRows, likedOns]
  elif language == 'Any language' and accent != 'Any accent':
    accentAudioRows = []
    likedOns = []
    for audioRow in audioRows:
      if audioRow['accent'] == accent:
        accentAudioRows.append(audioRow)
        likedOns.append(app_tables.likes.get(audioRow=audioRow, likedBy=user)['likedOn'].date())
    return [accentAudioRows, likedOns]
  elif language != 'Any language' and accent == 'Any accent':
    languageAudioRows = []
    likedOns = []
    for audioRow in audioRows:
      if audioRow['language'] == language:
        languageAudioRows.append(audioRow)
        likedOns.append(app_tables.likes.get(audioRow=audioRow, likedBy=user)['likedOn'].date())
    return [languageAudioRows, likedOns]
  else:
    languageAccentAudioRows = []
    likedOns = []
    for audioRow in audioRows:
      if audioRow['language'] == language and audioRow['accent'] == accent:
        languageAudioRows.append(audioRow)
        likedOns.append(app_tables.histories.get(audioRow=audioRow, likedBy=user)['likedOn'].date())
    return [languageAccentAudioRows, likedOns]


@anvil.server.callable
def clear_liked():
  """Clear the liked dubs"""
  user = anvil.users.get_user()
  if user is not None:
    listOfLiked = app_tables.likes.search(likedBy=user)
    for liked in listOfLiked:
      try:
        likes = liked['audioRow']['likes'] - 1
        liked['audioRow'].update(likes=likes)
        liked.delete()
      except Exception:
        liked.delete()


@anvil.server.callable
def save_transcript(videoID, videoTitle, languageCode, transcriptItem):
  """Save the translated transcript to the database"""
  user = anvil.users.get_user()
  videoUrl = 'https://www.youtube.com/watch?v=' + videoID
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  if videoRow is None:
    try:
      app_tables.videos.add_row(videoTitle=videoTitle, videoUrl=videoUrl, youTubeVideoID=videoID)
      videoRow = app_tables.videos.get(youTubeVideoID=videoID)
    except Exception:
      return False
  transcript = app_tables.transcripts.get(createdBy=user, languageCode=languageCode, video=videoRow)
  if transcript is None:
    try:
      app_tables.transcripts.add_row(createdBy=user, createdOn=datetime.now(), languageCode=languageCode, video=videoRow, transcript=transcriptItem)
      return True
    except Exception:
      return False
  else:
    try:
      transcript.update(createdOn=datetime.now(), transcript=transcriptItem)
      return True
    except Exception:
      return False


@anvil.server.callable
def check_transcript(languageCode, videoID):
  """Check whether transcript for the video existed in the database"""
  user = anvil.users.get_user()
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  if videoRow is None:
    return None
  else:
    transcriptRow = app_tables.transcripts.get(createdBy=user, languageCode=languageCode, video=videoRow)
    if transcriptRow is None:
      return None
    else:
      return transcriptRow['transcript']


@anvil.server.callable
def delete_transcript(languageCode, videoID):
  """Delete the transcript of the video specified by the language code"""
  user = anvil.users.get_user()
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  if videoRow is None:
    return None
  else:
    transcriptRow = app_tables.transcripts.get(createdBy=user, languageCode=languageCode, video=videoRow)
    if transcriptRow is None:
      return None
    else:
      transcriptRow.delete()
      return True


@anvil.server.callable
def check_accompaniment(videoID):
  """Check whether the accompaniment of a video is saved in the database"""
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  if videoRow is None:
    return False
  else:
    if videoRow['accompaniment'] is None:
      return False
    else:
      return True


@anvil.server.callable
def check_temp_dub(languageCode, videoID):
  """Check whether there is unpublished dub for the video in the specified language"""
  user = anvil.users.get_user()
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  transcriptRow = app_tables.transcripts.get(createdBy=user, languageCode=languageCode, video=videoRow)
  if transcriptRow['dub'] is None:
    return None
  else:
    return transcriptRow


@anvil.server.callable
def get_saved_transcript(languageCode, videoID):
  """Check whether transcript for the video existed in the database"""
  user = anvil.users.get_user()
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  if videoRow is None:
    return None
  else:
    transcriptRow = app_tables.transcripts.get(createdBy=user, languageCode=languageCode, video=videoRow)
    if transcriptRow is None:
      return None
    else:
      return transcriptRow['transcript']


@anvil.server.callable
def delete_tempDub(languageCode, videoID):
  """Delete the unpublished dub"""
  user = anvil.users.get_user()
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  transcriptRow = app_tables.transcripts.get(createdBy=user, languageCode=languageCode, video=videoRow)
  if transcriptRow is None:
    return False
  else:
    transcriptRow.update(dub=None, accent=None)
    return True


@anvil.server.callable
def add_upload_dub_to_transcript(languageCode, videoID, dub, accent):
  """Add the uploaded audio as unpublished dub"""
  user = anvil.users.get_user()
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  transcriptRow = app_tables.transcripts.get(createdBy=user, languageCode=languageCode, video=videoRow)
  if transcriptRow is None:
    return False
  else:
    transcriptRow.update(dub=dub, accent=accent)
    return True


@anvil.server.callable
def check_dub_existed(languageCode, videoID, language):
  """Check whether dub existed for the video in the specified language"""
  user = anvil.users.get_user()
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  transcriptRow = app_tables.transcripts.get(createdBy=user, languageCode=languageCode, video=videoRow)
  if transcriptRow is None:
    return False
  else:
    if transcriptRow['dub'] is None:
      return False
    audio_dict = {'language': language, 'accent': transcriptRow['accent'], 'audio': transcriptRow['dub']}
    audioRow = app_tables.audios.get(language=audio_dict['language'], accent=audio_dict['accent'], videoUrl=videoRow, createdBy=user)
    if audioRow is None:
      return False
    else:
      return True


@anvil.server.callable
def check_dub_existed2(audio_dict):
  """Check whether a dub exists and return the dub row if exists"""
  user = anvil.users.get_user()
  youTubeVideoTitle = anvil.server.call('get_video_title_from_url', audio_dict['videoUrl'])
  if youTubeVideoTitle is not None:
    videoID = get_video_id_from_url(audio_dict['videoUrl'])
    videoRow = app_tables.videos.get(youTubeVideoID=videoID)
    audioRow = app_tables.audios.get(language=audio_dict['language'], accent=audio_dict['accent'], videoUrl=videoRow, createdBy=user)
    if audioRow is None:
      return None
    else:
      return audioRow
  else:
    return False


@anvil.server.callable
def publish(languageCode, videoID, language):
  """Publish the unpublished dub"""
  user = anvil.users.get_user()
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  transcriptRow = app_tables.transcripts.get(createdBy=user, languageCode=languageCode, video=videoRow)
  # oldDub = []
  if transcriptRow is None:
    return False
  else:
    if transcriptRow['dub'] is None:
      return False
    audio_dict = {'language': language, 'accent': transcriptRow['accent'], 'audio': transcriptRow['dub']}
    audioRow = app_tables.audios.get(language=audio_dict['language'], accent=audio_dict['accent'], videoUrl=videoRow, createdBy=user)
    if audioRow is not None:
      # oldDub = audioRow['audio']
      delete_audio(audioRow)
    allAudioRows = app_tables.audios.search()
    if len(allAudioRows) > 0:
      lastAudioID = str(allAudioRows[len(allAudioRows)-1]['audioID'])
      idNumber = int(lastAudioID[1:]) + 1
      newAudioID = "a" + str(idNumber)
      success = add_audio_helper(newAudioID, user, videoRow, audio_dict)
    else:
      newAudioID = "a1"
      success = add_audio_helper(newAudioID, user, videoRow, audio_dict)
    if success:
      transcriptRow.update(dub=None, accent=None)
      # if oldDub == []:
      return True
      # else:
        # return oldDub
    else:
      return False
    

@anvil.server.callable
def get_paypal_link(user):
  """Get the link to the PayPal page"""
  paypal_link = app_tables.links.get(socialMediaName='PayPal', user=user)
  if paypal_link is None:
    return None
  else:
    return paypal_link['link']


@anvil.server.callable
def delete_user(user):
  """Delete everything related to the user and the user account"""
  if user == anvil.users.get_user():
    createdDubs = app_tables.audios.search(createdBy=user)
    if len(createdDubs) > 0:
      for dub in createdDubs:
        
        flags = app_tables.flags.search(audioRow=dub)
        if len(flags) > 0:
          for flag in flags:
            flag.delete()
        likes = app_tables.likes.search(audioRow=dub)
        if len(likes) > 0:
          for like in likes:
            like.delete()
        dislikes = app_tables.dislikes.search(audioRow=dub)
        if len(dislikes) > 0:
          for dislike in dislikes:
            dislike.delete()
        histories = app_tables.histories.search(audioRow=dub)
        if len(histories) > 0:
          for history in histories:
            history.delete()
        
        dub.delete()

    likes = app_tables.likes.search(likedBy=user)
    if len(likes) > 0:
      for like in likes:
        like.delete()

    dislikes = app_tables.dislikes.search(dislikedBy=user)
    if len(dislikes) > 0:
      for dislike in dislikes:
        dislike.delete()

    flags = app_tables.flags.search(flaggedBy=user)
    if len(flags) > 0:
      for flag in flags:
        flag.delete()

    histories = app_tables.histories.search(listenedBy=user)
    if len(histories) > 0:
      for history in histories:
        history.delete()

    links = app_tables.links.search(user=user)
    if len(links) > 0:
      for link in links:
        link.delete()

    requests = app_tables.requests.search(requestedBy=user)
    if len(requests) > 0:
      for request in requests:
        request.delete()

    subscribers = app_tables.subscriptions.search(userID=user)
    if len(subscribers) > 0:
      for subscriber in subscribers:
        subscriber.delete()

    subscriptions = app_tables.subscriptions.search(subscribedBy=user)
    if len(subscriptions) > 0:
      for subscription in subscriptions:
        subscription.delete()

    transcripts = app_tables.transcripts.search(createdBy=user)
    if len(transcripts) > 0:
      for transcript in transcripts:
        transcript.delete()

    anvil.users.get_user().delete()
    return True
  else:
    return False


@anvil.server.callable
def block_unblock_dub(audioRow, reason=None):
  """Block or unblock a dub (Admin's function)"""
  user = anvil.users.get_user()
  if user['admin']:
    if audioRow['blocked']:
      audioRow.update(blocked=False, blockReason=reason)
      emailText = "Your dub for the video: [" + audioRow['videoTitle'] + "] in the language: [" + audioRow['language'] + "] and accent: [" + audioRow['accent'] + "] has been unblocked by the admin of DubTube."
      anvil.email.send(from_name = "DubTubeAdmin", 
                 to = audioRow['createdBy']['email'],
                 subject = "Your dub has been unblocked by DubTube's admin",
                 text = emailText)
    else:
      audioRow.update(blocked=True, blockReason=reason)
      emailText = "Your dub for the video: [" + audioRow['videoTitle'] + "] in the language: [" + audioRow['language'] + "] and accent: [" + audioRow['accent'] + "] has been blocked by the admin of DubTube due to: [" + reason + "].\n"
      emailText += "Please edit your dub as soon as possible to get unblocked. Thank you."
      anvil.email.send(from_name = "DubTubeAdmin", 
                 to = audioRow['createdBy']['email'],
                 subject = "Your dub has been blocked by DubTube's admin",
                 text = emailText)


@anvil.server.callable
def check_block():
  """Check whether there are any blocked dubs for the current user"""
  user = anvil.users.get_user()
  audioRows = app_tables.audios.search(createdBy=user, blocked=True)
  if len(audioRows) > 0:
    return True
  else:
    return False


@anvil.server.callable
def get_subtitle(videoRow, audioID):
  """Get the transcript for the dub"""
  audioRow = app_tables.audios.get(audioID=audioID)
  createdBy = audioRow['createdBy']
  languageCode = languages_mapping.get(audioRow['language'])
  transcriptRow = app_tables.transcripts.get(video=videoRow, createdBy=createdBy, languageCode=languageCode)
  if transcriptRow is None:
    return None
  else:
    return transcriptRow['transcript']


@anvil.server.callable
def get_video_page_subtitle(audioID):
  """Get the subtitle that will be used in the video page"""
  audioRow = app_tables.audios.get(audioID=audioID)
  languageCode = languages_mapping[audioRow['language']]
  videoRow = audioRow['videoUrl']
  createdBy = audioRow['createdBy']
  transcriptRow = app_tables.transcripts.get(createdBy=createdBy, video=videoRow, languageCode=languageCode)
  if transcriptRow is not None:
    transcript = transcriptRow['transcript']
    for line in transcript:
      start_time_seconds = line["startMin"] * 60 + line["startSec"]
      end_time_seconds = line["endMin"] * 60 + line["endSec"]
      line["start"] = start_time_seconds
      line["end"] = end_time_seconds
      line.pop("startMin")
      line.pop("startSec")
      line.pop("endMin")
      line.pop("endSec")
    return transcript
  else:
    return None


@anvil.server.callable
def check_request_response():
  """Check whether there is any dub request by the current user that has been responded"""
  user = anvil.users.get_user()
  requests = app_tables.requests.search(requestedBy=user, responded=True)
  if len(requests) > 0:
    return True
  else:
    return False


@anvil.server.callable
def dub_for_request(videoUrl, language, accent):
  """Get the dub for the request"""
  user = anvil.users.get_user()
  requestRow = app_tables.requests.get(requestedBy=user, requestAccent=accent, requestLanguage=language, requestVideoUrl=videoUrl)
  requestRow.update(responded=False, checked=True)
  videoRow = app_tables.videos.get(videoUrl=videoUrl)
  if accent == 'Any accent':
    audioRows = app_tables.audios.search(language=language, videoUrl=videoRow)
    return audioRows[0]
  else:
    audioRows = app_tables.audios.search(language=language, accent=accent, videoUrl=videoRow)
    return audioRows[0]


@anvil.server.callable
def get_blocked_dubs(language='Any language', accent='Any accent'):
  """Get the blocked dubs"""
  if language == 'Any language' and accent == 'Any accent':
    blockedDubRows = app_tables.audios.search(blocked=True)
  elif language != 'Any language' and accent == 'Any accent':
    blockedDubRows = app_tables.audios.search(blocked=True, language=language)
  elif language == 'Any language' and accent != 'Any accent':
    blockedDubRows = app_tables.audios.search(blocked=True, accent=accent)
  else:
    blockedDubRows = app_tables.audios.search(blocked=True, accent=accent, language=language)
  return blockedDubRows


@anvil.server.callable
def add_advertisement(ad_dict):
  """Add an advertisement application"""
  dateToday = datetime.today().date()
  date30DaysLater = dateToday + timedelta(days=30)
  adRows = app_tables.advertisements.search()
  counter = 0
  if len(adRows) > 0:
    for adRow in adRows:
      if adRow['shownOn'] is not None:
        if adRow['shownOn'] < dateToday:
          adRow.delete()
        elif adRow['shownOn'] < date30DaysLater:
          counter += 1
      else:
        if adRow['mightBeShownOn'] < dateToday:
          adRow.delete()
        elif adRow['mightBeShownOn'] < date30DaysLater:
          counter += 1
  if counter < 90:
    user = anvil.users.get_user()
    daysToAdd = counter//3
    possibleShownDate = dateToday + timedelta(days=daysToAdd)
    app_tables.advertisements.add_row(link=ad_dict['link'], advertisementPicture=ad_dict['advertisementPicture'], appliedBy=user, appliedOn=datetime.now(), status='Waiting', mightBeShownOn=possibleShownDate, statusRead=False)
    return True
  else:
    return False


@anvil.server.callable
def update_advertisement(adRow, ad_dict):
  """Update the advertisement application"""
  if app_tables.advertisements.has_row(adRow):
    adRow.update(advertisementPicture=ad_dict['advertisementPicture'], link=ad_dict['link'])
    return True
  else:
    return False


@anvil.server.callable
def delete_advertisement(adRow):
  """Delete the advertisement application"""
  if app_tables.advertisements.has_row(adRow):
    adRow.delete()
    return True
  else:
    return False
    

@anvil.server.callable
def get_advertisement():
  """Get the advertisement application"""
  dateToday = datetime.today().date()
  date30DaysLater = dateToday + timedelta(days=30)
  adRows = app_tables.advertisements.search()
  counter = 0
  if len(adRows) > 0:
    for adRow in adRows:
      if adRow['shownOn'] is not None:
        if adRow['shownOn'] < dateToday:
          adRow.delete()
        elif adRow['shownOn'] < date30DaysLater:
          counter += 1
      else:
        # if adRow['mightBeShownOn'] < dateToday:
        #   adRow.delete()
        if adRow['mightBeShownOn'] < date30DaysLater:
          counter += 1
  user = anvil.users.get_user()
  adRows = app_tables.advertisements.search(tables.order_by('appliedOn', ascending=False), appliedBy=user)
  return adRows, 90-counter


@anvil.server.callable
def get_today_advertisement():
  """Get today's advertisement"""
  dateToday = datetime.today().date()
  adRows = app_tables.advertisements.search(tables.order_by('appliedOn', ascending=False), shownOn=dateToday, status='Approved')
  linkAndPicture = []
  if len(adRows) > 0:
    for adRow in adRows:
      linkAndPicture.append({'advertisementPicture': adRow['advertisementPicture'], 'link': adRow['link']})
  while len(linkAndPicture) < 3:
    linkAndPicture.append({'advertisementPicture': None, 'link': None})
  return linkAndPicture


@anvil.server.callable
def get_waiting_advertisement():
  """Get waiting advertisement application"""
  dateToday = datetime.today().date()
  date30DaysLater = dateToday + timedelta(days=30)
  adRows = app_tables.advertisements.search()
  counter = 0
  if len(adRows) > 0:
    for adRow in adRows:
      if adRow['shownOn'] is not None:
        if adRow['shownOn'] < dateToday:
          adRow.delete()
        elif adRow['shownOn'] < date30DaysLater:
          counter += 1
      # else:
      #   if adRow['mightBeShownOn'] < dateToday:
      #     adRow.delete()
  adRows = app_tables.advertisements.search(tables.order_by('appliedOn', ascending=True), status='Waiting')
  return adRows, 90-counter


@anvil.server.callable
def get_accepted_advertisement():
  """Get accepted advertisement"""
  adRows = app_tables.advertisements.search(tables.order_by('acceptedOn', ascending=True), status='Accepted')
  return adRows


@anvil.server.callable
def get_approved_advertisement():
  adRows = app_tables.advertisements.search(tables.order_by('approvedOn', ascending=True), status='Approved')
  return adRows


@anvil.server.callable
def accept_advertisement(adRow):
  """Accept advertisement application"""
  user = anvil.users.get_user()
  if user['admin']:
    if app_tables.advertisements.has_row(adRow):
      adRow.update(acceptedBy=user, acceptedOn=datetime.now(), status='Accepted', statusRead=False)
      html = 'Your advertisement application for the link: [<a href="' + adRow['link'] + '">' + adRow['link'] + '</a>] has been accepted. <br/><br/> Please pay 1 USD to DubTube via this PayPal link: '
      html += '[<a href="https://www.paypal.com/donate/?hosted_button_id=ZHM7JT2V9UV2N">PayPal</a>] to get your advertisement approved.'
      anvil.email.send(from_name = "DubTubeAdmin", 
                to = adRow['appliedBy']['email'],
                subject = "[DubTube] Your advertisement application has been accepted",
                html = html)
      return True
    else:
      return False


@anvil.server.callable
def reject_advertisement(adRow):
  """Reject the advertisement application"""
  if anvil.users.get_user()['admin']:
    if app_tables.advertisements.has_row(adRow):
      adRow.update(status='Rejected', statusRead=False)
      html = 'Sorry. Your advertisement application for the link: [<a href="' + adRow['link'] + '">' + adRow['link'] + '</a>] has been rejected.'
      anvil.email.send(from_name = "DubTubeAdmin", 
                to = adRow['appliedBy']['email'],
                subject = "[DubTube] Your advertisement application has been rejected",
                html = html)
      return True
  return False
  

@anvil.server.callable
def approve_advertisement(selectedAdRow):
  """Approve advertisement application after receiving money"""
  dateToday = datetime.today().date()
  date30DaysLater = dateToday + timedelta(days=30)
  adRows = app_tables.advertisements.search()
  counter = 0
  if len(adRows) > 0:
    for adRow in adRows:
      if adRow['shownOn'] is not None:
        if adRow['shownOn'] < dateToday:
          adRow.delete()
        elif adRow['shownOn'] < date30DaysLater:
          counter += 1
  if counter < 90:
    user = anvil.users.get_user()
    daysToAdd = counter//3
    shownDate = dateToday + timedelta(days=daysToAdd)
    if app_tables.advertisements.has_row(selectedAdRow):
      selectedAdRow.update(approvedBy=user, approvedOn=datetime.now(), status='Approved', shownOn=shownDate, statusRead=False)
      html = 'Your advertisement application for the link: [<a href="' + adRow['link'] + '">' + adRow['link'] + '</a>] has been approved.'
      html += '<br/><br/>It will be shown on: [' + str(shownDate) + '].'
      anvil.email.send(from_name = "DubTubeAdmin", 
                to = adRow['appliedBy']['email'],
                subject = "[DubTube] Your advertisement application has been approved",
                html = html)
      return True
    else:
      return False
  else:
    return False


@anvil.server.callable
def check_ads_accepted_approved():
  """Check whether advertisement application is accepted or approved"""
  user = anvil.users.get_user()
  if user is not None:
    if user['admin'] is False:
      acceptedAdRows = app_tables.advertisements.search(appliedBy=user, status='Accepted', statusRead=False)
      if len(acceptedAdRows) > 0:
        return True
      approvedAdRows = app_tables.advertisements.search(appliedBy=user, status='Approved', statusRead=False)
      if len(approvedAdRows) > 0:
        return True
  return False


@anvil.server.callable
def mark_ads_as_read():
  """Change the read status of the advertisement applications created by the current user to True"""
  user = anvil.users.get_user()
  adRows = app_tables.advertisements.search(appliedBy=user)
  if len(adRows) > 0:
    for adRow in adRows:
      adRow.update(statusRead=True)


@anvil.server.callable
def get_top_ten():
  """Get the users with the top ten performance"""
  today = datetime.now()
  # print(today.day)
  topTens = app_tables.topten.search(tables.order_by('place', ascending=True))
  if today.day == 1 or len(topTens) == 0:
    determine_top_ten()
    topTens = app_tables.topten.search(tables.order_by('place', ascending=True))
    return topTens
  else:
    return topTens


@anvil.server.callable
def determine_top_ten():
  """Determine the top ten based on the previous month dub row, subscriptions, likes, listens, """
  today = datetime.now()
  if today.month != 1:
    first_day_of_previous_month = datetime(today.year, today.month - 1, 1).date()
    last_day_of_previous_month = (datetime(today.year, today.month, 1) - timedelta(days=1)).date()
  else:
    first_day_of_previous_month = datetime(today.year - 1, 12, 1).date()
    last_day_of_previous_month = (datetime(today.year, today.month, 1) - timedelta(days=1)).date()
  
  dubRows = app_tables.audios.search()
  previous_month_dubRows = [dubRow for dubRow in dubRows if first_day_of_previous_month <= dubRow['createdOn'].date() < last_day_of_previous_month]
  # Count occurrences of each 'createdBy' value
  createdBy_counts = Counter(item['createdBy'] for item in previous_month_dubRows)
  eligibleUsers = [{'user': key, 'numberOfDubs': value} for key, value in createdBy_counts.items() if value >= 2]
  
  subscriptionRows = app_tables.subscriptions.search()
  previous_month_subscriptionRows = [subscriptionRow for subscriptionRow in subscriptionRows if first_day_of_previous_month <= subscriptionRow['subscribedOn'].date() < last_day_of_previous_month]
  subscription_counts = Counter(item['userID'] for item in previous_month_subscriptionRows)
  for key, value in subscription_counts.items():
    for eligibleUser in eligibleUsers:
      if key == eligibleUser['user']:
        eligibleUser['newSubscribers'] = value
  
  likeRows = app_tables.likes.search()
  previous_month_likeRows = [likeRow for likeRow in likeRows if first_day_of_previous_month <= likeRow['likedOn'].date() < last_day_of_previous_month]
  like_counts = Counter(item['audioRow']['createdBy'] for item in previous_month_likeRows)
  for key, value in like_counts.items():
    for eligibleUser in eligibleUsers:
      if key == eligibleUser['user']:
        eligibleUser['newLikes'] = value

  listenRows = app_tables.histories.search()
  previous_month_listenRows = [listenRow for listenRow in listenRows if first_day_of_previous_month <= listenRow['listenedOn'].date() < last_day_of_previous_month]
  listen_counts = Counter(item['audioRow']['createdBy'] for item in previous_month_listenRows)
  for key, value in listen_counts.items():
    for eligibleUser in eligibleUsers:
      if key == eligibleUser['user']:
        eligibleUser['newListens'] = value

  # Each new subscriber 5 marks, new like 3 marks, new listen 1 mark
  for eligibleUser in eligibleUsers:
    eligibleUser['marks'] = eligibleUser['newSubscribers']*5 + eligibleUser['newLikes']*3 + eligibleUser['newListens']

  topTens = sorted(eligibleUsers, key=lambda x: x['marks'], reverse=True)
  if len(topTens) > 10:
    topTens = topTens[:10]

  marks_sum = sum(topTen['marks'] for topTen in topTens)
  place = 1
  for topTen in topTens:
    topTen['place'] = place
    percentage = round((topTen['marks'] / marks_sum) * 100)
    topTen['percentage'] = percentage
    place += 1

  previous_topTens = app_tables.topten.search()
  if len(previous_topTens) > 0:
    for previous_topTen in previous_topTens:
      previous_topTen.delete()
  for topTen in topTens:
    app_tables.topten.add_row(creator=topTen['user'], 
                              dubsCreated=topTen['numberOfDubs'], 
                              subscribersGained=topTen['newSubscribers'], 
                              likesGained=topTen['newLikes'], 
                              listensGained=topTen['newListens'], 
                              marks=topTen['marks'], 
                              percentage=topTen['percentage'], 
                              place=topTen['place'])
  

@anvil.server.callable
def get_accompaniment(videoUrl):
  """Get the accompaniment of a video"""
  videoID = get_video_id_from_url(videoUrl)
  videoRow = app_tables.videos.get(youTubeVideoID=videoID)
  if videoRow is not None:
    if videoRow['accompaniment'] is not None:
      return videoRow['accompaniment']
    else:
      return None
  else:
    return None


@anvil.server.callable
def get_channel_owner(profileName):
  """Get the channel owner"""
  return app_tables.users.get(profileName=profileName)


@anvil.server.callable
def get_audio_from_id(audioid):
  """Get the dub audio from its id"""
  audioRow = app_tables.audios.get(audioID=audioid)
  if audioRow is not None:
    return audioRow['audio']
  else:
    return None


@anvil.server.callable
def check_videoid_exist(videoid):
  """Check whether the video with the given video id exists in the database"""
  videoRow = app_tables.videos.get(youTubeVideoID=videoid)
  if videoRow is None:
    return False
  else:
    return True


  