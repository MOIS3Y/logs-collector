"""
An application for uploading archives with log files
for their subsequent download and check issues
that have arisen with software products.
The purpose of creating this application is
the ability to securely exchange and store log files containing sensitive data.
I have not found an application that would allow an unauthorized client
to upload data without providing him with authorization credentials.
You can use other applications for this,
such as Google cloud, Yandex cloud, DropBox etc, but in this case,
you do not have a tool that would allow you to automatically restrict uploads
later until you explicitly deny access to the shared link.
This app allows you to upload files using a unique token
associated with a support ticket.
This token has a limit on the number of file upload attempts.
Also, if the ticket is resolved, then the token is invalid.
"""


# █▀▄▀█ █▀▀ ▀█▀ ▄▀█ ▀
# █░▀░█ ██▄ ░█░ █▀█ ▄
# -------------------
__author__ = "MOIS3Y"
__credits__ = ["Stepan Zhukovsky"]
__license__ = "GPL v3.0"
__version__ = "0.1.0"
__maintainer__ = "Stepan Zhukovsky"
__email__ = "stepan@zhukovsky.me"
__status__ = "Development"
