#!/usr/bin/env python
"""Get count of unread emails."""

import imaplib
import netrc
import re
import subprocess


def get_unread_count():
    """Get count of unread emails."""
    login, _, password = netrc.netrc().authenticators('personal-gmail')
    connection = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    connection.login(login, password)
    status = connection.status('INBOX', '(UNSEEN)')[1][0].decode('utf-8')
    unread_count = re.search('UNSEEN (\d+)', status).group(1)
    return unread_count


def main():
    """Main function to print the count."""
    unread_count = get_unread_count()
    if unread_count:
        command = f'echo  {unread_count}'
    else:
        command = 'echo  '

    subprocess.run(command, shell=True)


if __name__ == '__main__':
    main()
