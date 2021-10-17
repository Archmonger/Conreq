"""
Tests for {{ verbose_name }}.

These will automatically be run at Conreq start up to ensure this app 
does not have any critical failures or misconfiguration.

See more information in the Django Tests and Channels Tests docs.
"""
from channels.testing import ChannelsLiveServerTestCase
from django.test import TestCase
