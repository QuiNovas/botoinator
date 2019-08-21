#!/usr/bin/env python3.7

import boto3
import botoinator
from moto import mock_s3, mock_sqs

""" This is our decorator that we will apply to boto3 methods """
def myDecorator(func):
  def test_decorator(*args, **kwargs):
    setattr(test_decorator, 'testValue', True)
    return func(*args, **kwargs)
  return test_decorator

@mock_s3
def testRegisterToClient():

  """
  Test registering a decorator to a single boto3 session
  """

  # Create a boto3 session
  s = boto3.session.Session()

  # Register the create_bucket() method to use our decorator for this session
  s.register_client_decorator('s3', 'create_bucket', myDecorator)

  # Now create our client as we normally would
  client1 = s.client('s3')

  # Now we can see that create_bucket() was decorated by testing the attribute we added
  client1.create_bucket(Bucket='foo')
  assert hasattr(client1.create_bucket, 'testValue')

  # We can also see that this only applies to calls made by the session we registered by creating a new session through boto3.client() and not registering a decorator
  client2 = boto3.client('s3')
  client2.create_bucket(Bucket='foo')

  # Now we can see that client.create_bucket() is not decorated
  assert not hasattr(client2.create_bucket, 'testValue')

  # Remove the decorator from the session
  s.unregister_client_decorator('s3', 'create_bucket')

  # Now create a new client on the same session we created at first
  client3 = s.client('s3')
  client3.create_bucket(Bucket='bar')

  # The session should no longer be decorating methods for new clients
  assert not hasattr(client3.create_bucket, 'testValue1')


testRegisterToClient()
