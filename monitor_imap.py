#!/usr/bin/env python
import time
import sys
import os
import subprocess

import logging
from imbox import Imbox

import dirutils # some common directory checks library
import transfer_config as conf
import send_confirmation_email as send_confirm

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

def login_imbox():
    """
    Sets up the mail inbox to check
    """
    mail_login = Imbox('imap.gmail.com',
                  conf.account_username,
                  conf.account_pass,
                  ssl=True)
    return mail_login


def monitor_loop():
    logger.debug("Checking messages")
    #First the mail box is queried, obtaining any new message IDs.
    mail_login = login_imbox()
    new_uids = mail_login.query_uids(sent_from=conf.special_message_sender,
                                unread=True
                                )
    files = {}  # Define a dictionary to store the files to download (stores files from multiple emails)
    n_magic = len(conf.magic_subject_words)     #Set the length of the magic subjects words from the conf file
    # Now the messages found before are actually read, checking if we want them.
    for u in new_uids:
        msg = mail_login.fetch_by_uid(u) 
        # The if statement below is checking if the first n words match the magic subject words
        # and also if the entire subject line has 3 words after (manually set - come back to)
        if (msg.subject.split()[:n_magic] == conf.magic_subject_words
            and len(msg.subject.split()) == n_magic + 3
            ):
            tempsplit=msg.body['plain'][0].split("\r\n") # read the message body and split it to get info
            obslength=float(tempsplit[2].split(" = ")[-1]) # Unique to CHILES, I fetch the observation length from the body
            # (The Obs length is used later when organising the files - ignore commented lines below)
            # for t in tempsplit:
                # if "SB length (hr)" in t:
                    # obslength=float(t.split(" = ")[-1])
            filetoget = msg.body['plain'][0].rstrip().split()[0] # another split to get the filename (check why)
            filename = filetoget.split("/")[-1] # Get the name of the file
            logger.debug("Matching message found, file name: {}".format(filename))
            # Add file to files dictionary
            files[u] = [filetoget,filename,obslength, msg.subject]
            # Now important to mark the message as read - otherwise if the transfer takes longer than the next check, 
            # the file will be attempted to download again.
            mail_login.mark_seen(u) # Need this here in case transfers take longer than 1 hour
        else:
            logger.debug("Boooo:" + str(msg.subject)) # Report a non-message match
    
    dirutils.ensure_dir(conf.file_dest) # check the destination exists
    
    #begin the transferring
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
            # print cmd
            subprocess.check_call(cmd, shell=True)
            logging.info("Transferred " + fname[1] + " successfully.")
            problem=False
        except Exception as e:  #if there is a problem in transferring an error is raised
            logging.error("Error transferring file: " + fname[0])
            logging.error("Error reads:" + str(e))
            problem=True
        # finally:
        #     mail_login.mark_seen(uid)
        
        # Send the confirmation if the option is selected
        if conf.send_confirmation_mail:
            try:
                sentto=send_confirm.send_confirmation(fname[1], problem, fname[3], to=conf.send_confirmation_to, cc=conf.cc_confirmation_to)
                # if not problem: # Currently I set this to not problem as I wanted a notification myself. I need to check this
                #     send_confirm.send_confirmation(fname[1], problem, subject="", to=conf.error_message_address)
                logging.info("Response email sent to {0}".format(sentto))
            except:
                logging.error("Response email not sent!")
    
    # Sort the files (if there were any)
    # This creates a text file in the location that 'spotter' is watching.
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
    # time.sleep(conf.wait_time_in_seconds) # You can make it loop but I prefer crontab



if __name__ == "__main__":
    # while True:
    monitor_loop()


