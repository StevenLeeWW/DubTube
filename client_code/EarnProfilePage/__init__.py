from ._anvil_designer import EarnProfilePageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
from datetime import datetime, timedelta


class EarnProfilePage(EarnProfilePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_top_tens()
    

  def refresh_top_tens(self):
    """Get the needed info for the page"""
    today = datetime.today()
    # Calculate the first day of the previous month
    first_day_of_previous_month = today.replace(day=1) - timedelta(days=1)
    # Extract the month and year of the previous month
    previous_month = first_day_of_previous_month.strftime('%B')
    year = first_day_of_previous_month.year
    self.label_month.text = previous_month
    self.label_year.text = year
    topTens = anvil.server.call('get_top_ten')
    if len(topTens) > 0:
      self.repeating_panel_top_ten.items = topTens
      self.column_panel_no_eligible.visible = False
      self.data_grid_top_ten.visible = True
    else:
      self.column_panel_no_eligible.visible = True
      self.data_grid_top_ten.visible = False
