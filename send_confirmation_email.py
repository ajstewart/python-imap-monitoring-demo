#!/usr/bin/env python
import os
import sys
import transfer_config as conf
import dirutils
from envelopes import Envelope, SMTP

def send_confirmation(file_name, problem, subject="", to="", cc="", account_name=conf.account_desc_name):
	if problem==True:
		to=conf.error_message_address
		if subject=="":
			sub=" ".join(conf.send_error_subject_words) + " " + file_name
		else:
			sub=" ".join(conf.send_error_subject_words)+" - "+subject
		text='File not downloaded'
	else:
		if to=="":
			to=conf.send_confirmation_to
		if subject=="":
			sub=" ".join(conf.send_magic_subject_words) + " " + file_name
		else:
			sub=" ".join(conf.send_magic_subject_words)+" - "+subject
		text='File Downloaded'
	msg = Envelope(to_addr=(to[0], to[1]),
	               from_addr=(conf.account_username, account_name),
	               subject=sub,
	               text_body=text)

	if cc!="":
		msg.add_cc_addr(cc)
	
	gmail = SMTP(host='smtp.googlemail.com', port=587,
	             login=conf.account_username, password=conf.account_pass, tls=True)

	gmail.send(msg)
	return to
	
if __name__=="__main__":
	f="test.txt"
	send_confirmation(f)
