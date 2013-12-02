#!/usr/bin/env python
import getpass
import base64


def prompt_for_pass():
    print "This script should be run via regular python interpreter."
    print "(Ipython will echo your password to the terminal!)"
    print "Now, please enter your password:"
    rawpass = getpass.getpass()
    encoded = base64.b64encode(rawpass)
    print "Your base64 obfuscated password is:"
    print encoded



if __name__ == "__main__":
    prompt_for_pass()
