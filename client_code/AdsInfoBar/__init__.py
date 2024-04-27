from ._anvil_designer import AdsInfoBarTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..AdvertisementEdit import AdvertisementEdit

class AdsInfoBar(AdsInfoBarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    # If the ad application is already accepted/approved/rejected, then it should be not editable anymore.
    if self.item['status'] == 'Accepted' or self.item['status'] == 'Approved' or self.item['status'] == 'Rejected':
      self.button_edit.enabled = False
    if self.item['status'] == 'Accepted':
      self.label_apply_title.text = 'Accepted on:'
      self.label_applied.text = self.item['acceptedOn'].date()
    if self.item['status'] == 'Approved':
      self.label_apply_title.text = 'Approved on:'
      self.label_applied.text = self.item['approvedOn'].date()
      self.label_show_title.text = 'Show date:'
      self.label_show.text = self.item['shownOn']
    # Admin cannot edit nor delete the ad application. Admin can only accept/reject/approve the applications.
    if anvil.users.get_user()['admin']:
      self.button_edit.visible = False
      self.button_withdraw.visible = False
      self.button_acceptApprove.visible = True
      self.button_reject.visible = True
      # Once approved, no further action can be taken.
      if self.item['status'] == 'Approved':
        self.button_acceptApprove.enabled = False
        self.button_reject.enabled = False
      # Once the application is accepted, admin cannot reject it.
      if self.item['status'] == 'Accepted':
        self.button_reject.enabled = False
    # For non-admin users, i.e., the ad applicants
    else:
      # Change the display based on the status
      if self.item['status'] == 'Approved':
        self.label_status_title.foreground = 'green'
        self.label_status.foreground = 'green'
      if self.item['status'] == 'Accepted':
        self.label_status_title.foreground = 'blue'
        self.label_status.foreground = 'blue'
      if self.item['status'] == 'Rejected':
        self.label_status_title.foreground = 'red'
        self.label_status.foreground = 'red'

  
  def button_edit_click(self, **event_args):
    """This method is called when the 'edit' button is clicked"""
    parameters = {'mode': 'update', 'link': self.item['link'], 'advertisementpicture': self.item['advertisementPicture']}
    ad_dict = alert(
      content=AdvertisementEdit(**parameters),
      large=True,
      buttons=[("Cancel", -1)],
    )
    # If the 'Cancel' button is not clicked
    if ad_dict != -1:
      success = anvil.server.call('update_advertisement', self.item, ad_dict)
      if success:
        Notification('Ad application updated successfully!', title='Success', style='success', timeout=3).show()
        self.parent.parent.parent.refresh_advertisement()
      else:
        Notification('Sorry. Fail to update the ad application.', title='Alert', style='warning', timeout=3).show()
    

  def button_withdraw_click(self, **event_args):
    """This method is called when the 'withdraw/delete' button is clicked"""
    if confirm('Do you want to delete the ad?'):
      success = anvil.server.call('delete_advertisement', self.item)
      if success:
        Notification('Ad deleted successfully!', title='Success', style='success', timeout=3).show()
        self.parent.parent.parent.refresh_advertisement()
      else:
        Notification('Sorry. Fail to delete the ad.', title='Alert', style='warning', timeout=3).show()

  
  def button_acceptApprove_click(self, **event_args):
    """This method is called when the 'accept/approve' button is clicked"""
    if self.item['status'] == 'Waiting':
      if confirm('Do you want to accept this ad?'):
        success = anvil.server.call('accept_advertisement', self.item)
        if success:
          Notification('Accepted.', style='success', title='Success', timeout=3).show()
          self.parent.parent.parent.parent.refresh_advertisement()
        else:
          Notification('Sorry. Fail to accept the ad.', style='warning', title='Alert', timeout=3).show()
    elif self.item['status'] == 'Accepted':
      if confirm('Do you want to approve this ad?'):
        success = anvil.server.call('approve_advertisement', self.item)
        if success:
          Notification('Approved.', style='success', title='Success', timeout=3).show()
          self.parent.parent.parent.parent.refresh_advertisement()
        else:
          Notification('Sorry. Fail to approve the ad.', style='warning', title='Alert', timeout=3).show()

  
  def button_reject_click(self, **event_args):
    """This method is called when the 'reject' button is clicked"""
    if confirm('Do you want to reject this ad?'):
      success = anvil.server.call('reject_advertisement', self.item)
      if success:
        Notification('Rejected.', style='success', title='Success', timeout=3).show()
        self.parent.parent.parent.parent.refresh_advertisement()
      else:
        Notification('Sorry. Fail to reject the ad.', style='warning', title='Alert', timeout=3).show()
    
    
