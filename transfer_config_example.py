import base64

account_username = 'email.address@gmail.com'
account_pass = base64.b64decode('dfshfksdjkhfgdsjkhgsdjk')
account_desc_name = 'CHILES Transients Adam'     #The name of the account (used for sending replies)
special_message_sender = 'secret.squirrel@gmail.com'
magic_subject_words = ['file', 'available']
# wait_time_in_seconds = 10

# file_source = 'localhost:/tmp/test_sourcedir'
file_dest = '/tmp/test_destdir'
monitor_dest= '/dir/to/put/notify/file'

#Choose to send an email back to sender when successful or to alternative address if transfer fails
send_confirmation_mail=True
#send_confirmation_to in the format of ['email@address.com', 'Person Name']
send_confirmation_to = [special_message_sender, "Person Name"]
#cc only requires email
cc_confirmation_to = "cc_address@email.com"
send_magic_subject_words = ['file', 'downloaded']
error_message_address= ['receive.error.address@gmail.com', 'Error Name']
send_error_subject_words = ['file','transfer','error']


