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
def testAddToClient():
  """
  Test adding/removing a decorator for all boto3 sessions created
  """

  # Register the create_bucket() method to use our decorator
  boto3.session.Session.add_client_decorator('s3', 'create_bucket', myDecorator)

  # Now we can see that create_bucket() was decorated for two different clients/sessions by testing the attribute we added
  clientA = boto3.Session().client('s3')
  clientA.create_bucket(Bucket='foo')

  clientB = boto3.Session().client('s3')
  clientB.create_bucket(Bucket='bar')

  assert hasattr(clientA.create_bucket, 'testValue')
  assert hasattr(clientB.create_bucket, 'testValue')

  # Remove our decorator and test that we are no longer calling it
  boto3.session.Session.remove_client_decorator('s3', 'create_bucket') # Have to unregister on the default session

  # Client is created off of a new session
  clientC = boto3.Session().client('s3')
  clientC.create_bucket(Bucket='baz')

  assert not hasattr(clientC.create_bucket, 'testValue')

testAddToClient()
