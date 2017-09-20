import base64

account_username = 'email.address@gmail.com'
account_pass = base64.b64decode('dfshfksdjkhfgdsjkhgsdjk')
special_message_sender = 'secret.squirrel@gmail.com'
magic_subject_words = ['file', 'available']
# wait_time_in_seconds = 10

file_source = 'localhost:/tmp/test_sourcedir'
file_dest = '/tmp/test_destdir'
monitor_dest= '/dir/to/put/notify/file'

#Choose to send an email back to sender when successful or to alternative address if transfer fails
send_confirmation_mail=True
send_confirmation_to = special_message_sender
cc_confirmation_to = ""
send_magic_subject_words = ['file', 'downloaded']
error_message_address= 'receive.error.address@gmail.com'
send_error_subject_words = ['file','transfer','error']


