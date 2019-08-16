import boto3
import sys


from .session import DecoratedSession


# Monkey patch to use our Session object instead of boto3's
boto3.session.Session = DecoratedSession

# Now take care of the reference in the boto3.__init__ module
setattr(boto3, 'Session', DecoratedSession)
