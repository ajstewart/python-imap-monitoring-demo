#!/usr/bin/env python
import os
import sys
import random
import transfer_config as conf
import dirutils
from envelopes import Envelope, SMTP

random_num = random.randint(1, 10000)

if conf.file_source.find('localhost:') == 0:
    test_sourcedir = conf.file_source[len('localhost:'):]
    print "Writing test file to ", test_sourcedir
else:
    "Need to set source to localhost for automated testing."

dirutils.ensure_dir(test_sourcedir)
filename_to_send = 'foo' + str(random_num) + '.txt'
with open(os.path.join(test_sourcedir, filename_to_send), 'wb') as f:
    f.write('Hello, world!')


msg = Envelope(to_addr=(conf.account_username, conf.account_username),
               from_addr=(conf.account_username, conf.account_username),
               subject=" ".join(conf.magic_subject_words + [filename_to_send]),
               text_body='Hello world')

print "Msg", msg


gmail = SMTP(host='smtp.googlemail.com', port=587,
             login=conf.account_username, password=conf.account_pass, tls=True)
# gmail = GMailSMTP(login=account_username, password=account_pass)
print "Connected?"
# print gmail

gmail.send(msg)
print "Sent!"
