"""
Example local settings file. Copy this file to local.py and change
these settings.

Modify USER1, PASS1, USER2, and PASS2 to desired string values.
"""

from requests.auth import HTTPBasicAuth

DOMAIN = "https://staging2.osf.io/"  # TODO should this variable be called something else?
API_PREFIX = "api/v2/"
URL = "{}{}".format(DOMAIN, API_PREFIX)  # e.g. https://staging2.osf.io/api/v2/

# Change these to a the id's of a public node and private node that were created by USER1.
PUBLIC_NODE_ID = 'bxsu6'  # TODO: specify what this node should have - e.g. variety of files to test file download
PRIVATE_NODE_ID = 'p8es7'

# Change these to the email and pw of the main user, who created the nodes
USER1 = ''
PASS1 = ''
AUTH1 = HTTPBasicAuth(USER1, PASS1)
USER1_ID = 'se6py'  # Jamie Hand

# Change these to the email and pw of a second user, who can't see the private node
USER2 = ''
PASS2 = ''
AUTH2 = HTTPBasicAuth(USER2, PASS2)
USER2_ID = 'cm98x'  # Jamie 2