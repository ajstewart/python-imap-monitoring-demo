#!/usr/bin/env python
import time
import sys
import os
import subprocess

import logging
from imbox import Imbox

import dirutils
import transfer_config as conf
import send_confirmation_email as send_confirm

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',)
logger = logging.getLogger(__name__)



def login_imbox():
    mail_login = Imbox('imap.gmail.com',
                  conf.account_username,
                  conf.account_pass)
    return mail_login


def monitor_loop():
    logger.debug("Checking messages")

    mail_login = login_imbox()
    new_uids = mail_login.query_uids(sent_from=conf.special_message_sender,
                                unread=True
                                )
    files = {}
    for u in new_uids:
        msg = mail_login.fetch_by_uid(u)
        n_magic = len(conf.magic_subject_words)
        if (msg.subject.split()[:n_magic] == conf.magic_subject_words
            and len(msg.subject.split()) == n_magic + 1
            ):
            filename = msg.subject.split()[n_magic]
            logger.debug("Matching message found, file name: %s" %
                         filename)
            files[u] = filename
        else:
            logger.debug("Boooo:" + str(msg.subject))
    dirutils.ensure_dir(conf.file_dest)
    for uid, fname in files.iteritems():
        logging.debug("Transferring " + fname)
        src = os.path.join(conf.file_source, fname)
        dest = os.path.join(conf.file_dest, fname)
#         args= ['rsync', '-rav ']
#         args.append(src)
#         args.append(dest)
        cmd = ' '.join(('wget', src, dest))
        try:
            print cmd
            subprocess.check_call(cmd, shell=True)
            logging.info("Transferred " + fname + " successfully.")
            problem=False
        except Exception as e:
            logging.error("Error transferring file:" + fname)
            logging.error("Error reads:" + str(e))
            problem=True
        finally:
            mail_login.mark_seen(uid)
        if conf.send_confirmation_mail:
            try:
                sentto=send_confirm.send_confirmation(fname, problem)
                logging.info("Response email sent to {0}".format(sentto))
            except:
                logging.error("Response email not sent!")
    if len(files.values)>0:
		logger.debug("Processing recieved files")
	    for f in sorted(files.values()):
	        workfile=os.path.join(dest, f)
	        subprocess.call("echo PUT SCRIPT HERE {0}".format(workfile), shell=True)
    logger.debug("Going to sleep.")
    mail_login.logout()
    time.sleep(conf.wait_time_in_seconds)



if __name__ == "__main__":
    while True:
        monitor_loop()


