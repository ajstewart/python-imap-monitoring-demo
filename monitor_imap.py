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

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

def login_imbox():
    mail_login = Imbox('imap.gmail.com',
                  conf.account_username,
                  conf.account_pass,
                  ssl=True)
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
            and len(msg.subject.split()) == n_magic + 3
            ):
            tempsplit=msg.body['plain'][0].split("\r\n")
            obslength=float(msg.body['plain'][0].split("\r\n")[2].split(" = ")[-1])
            # for t in tempsplit:
                # if "SB length (hr)" in t:
                    # obslength=float(t.split(" = ")[-1])
            filetoget = msg.body['plain'][0].rstrip().split()[0]
            filename = filetoget.split("/")[-1]
            logger.debug("Matching message found, file name: %s" %
                         filename)
            files[u] = [filetoget,filename,obslength, msg.subject]
            mail_login.mark_seen(u) #Need this here in case transfers take longer than 1 hour
        else:
            logger.debug("Boooo:" + str(msg.subject))
    dirutils.ensure_dir(conf.file_dest)
    for uid, fname in files.iteritems():
        logging.debug("Transferring " + fname[1])
        src = fname[0]
        dest = os.path.join(conf.file_dest)
#         args= ['rsync', '-rav ']
#         args.append(src)
#         args.append(dest)
        cmd = ' '.join(('wget', '-P {0}'.format(dest), src))
    # cmd = ' '.join(('cp', '-r', src, dest))
        try:
            print cmd
            subprocess.check_call(cmd, shell=True)
            logging.info("Transferred " + fname[1] + " successfully.")
            problem=False
        except Exception as e:
            logging.error("Error transferring file: " + fname[0])
            logging.error("Error reads:" + str(e))
            problem=True
        # finally:
        #     mail_login.mark_seen(uid)
        if conf.send_confirmation_mail:
            try:
                sentto=send_confirm.send_confirmation(fname[1], problem, fname[3])
                if not problem:
                    send_confirm.send_confirmation(fname[1], problem, subject="", to=conf.error_message_address)
                logging.info("Response email sent to {0}".format(sentto))
            except:
                logging.error("Response email not sent!")
    if len(files.values())>0:
    logger.debug("Processing recieved files")
    for f in sorted(files.values()):
        # if "NO-SELFCAL" in msg.subject:
        workfile=os.path.join(conf.monitor_dest, f[1]+"-{0}-".format(f[2]))
        # else:
            # workfile=os.path.join(conf.monitor_dest, f[1]+"-SELFCAL-")
        subprocess.call("touch {0}.NEW".format(workfile), shell=True)
    # logger.debug("Going to sleep.")
    logger.debug("Quitting...")
    logger.debug("See you in an hour.")
    mail_login.logout()
    # time.sleep(conf.wait_time_in_seconds)



if __name__ == "__main__":
    # while True:
    monitor_loop()


