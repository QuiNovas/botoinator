#!/usr/bin/env python3.7

import boto3
import botoinator
from moto import mock_s3, mock_sqs
import time
import inspect

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

@mock_sqs
def testRegisterToResource():

  """
  Test registering a decorator to a single boto3 session
  """

  # Create a boto3 session
  s = boto3.session.Session()

  # Register the delete() method of SQS.Queue resource to be decorated for this session
  s.register_resource_decorator('sqs', 'Queue', 'delete', myDecorator)

  # Create our resource and a queue
  sqs1 = s.resource('sqs', region_name='us-east-1')
  sqs1.create_queue(QueueName='foo')
  # Check that our decorator was called by testing the testValue attribute to SQS.Queue.delete() method
  queue1 = sqs1.Queue('foo')
  queue1.delete('foo')
  assert hasattr(queue1.delete, 'testValue')

  # Test that decorator only applies to calls made by the session we registered by creating a new session through boto3.resource() and not registering a decorator
  sqs2 = boto3.resource('sqs', region_name='us-east-1')
  sqs2.create_queue(QueueName='bar')
  queue2 = sqs2.Queue('bar')
  queue2.delete('bar')
  assert not hasattr(queue2.delete, 'testValue')

@mock_s3
def testAddToClient():

  """
  Test registering a decorator to all boto3 sessions created
  """

  # Register the create_bucket() method to use our decorator
  boto3.session.Session.add_client_decorator('s3', 'create_bucket', myDecorator)

  # Now we can see that create_bucket() was decorated for two different clients/sessions by testing the attribute we added
  clientA = boto3.client('s3')
  clientA.create_bucket(Bucket='foo')

  clientB = boto3.client('s3')
  clientB.create_bucket(Bucket='bar')

  assert hasattr(clientA.create_bucket, 'testValue')
  assert hasattr(clientB.create_bucket, 'testValue')

  # Remove our decorator and test that we are no longer calling it
  boto3.DEFAULT_SESSION.unregister_client_decorator('s3', 'create_bucket') # Have to unregister on the default session
  clientC = boto3.client('s3')
  clientC.create_bucket(Bucket='baz')

  assert not hasattr(clientC.create_bucket, 'testValue')

@mock_sqs
def testAddToResource():

  """
  Test registering a decorator to all boto3 sessions created
  """

  # Register the create_bucket() method to use our decorator
  boto3.session.Session.add_resource_decorator('sqs', 'Queue', 'delete', myDecorator)

  # Create two clients
  sqs1 = boto3.resource('sqs', region_name='us-east-1')
  sqs2 = boto3.resource('sqs', region_name='us-east-1')

  # Create a queue to test with
  sqs1.create_queue(QueueName='foo')
  queue1 = sqs1.Queue('foo')
  queue1.delete('foo')

  sqs2.create_queue(QueueName='bar')
  queue2 = sqs2.Queue('bar')
  queue2.delete('bar')

  # Test that our decorator was called by testing the testValue attribute to SQS.Queue.delete() method
  assert hasattr(queue1.delete, 'testValue')
  assert hasattr(queue2.delete, 'testValue')

  # Remove our decorator so future sessions are not decorated
  boto3.DEFAULT_SESSION.unregister_resource_decorator('sqs', 'Queue', 'delete')
  sqs3 = boto3.resource('sqs', region_name='us-east-1')
  sqs3.create_queue(QueueName='baz')
  queue3 = sqs2.Queue('baz')
  queue3.delete('baz')

  # Should not have decorated
  assert not hasattr(queue3.delete, 'testValue')


testRegisterToClient()
boto3.DEFAULT_SESSION = None
testRegisterToResource()
boto3.DEFAULT_SESSION = None
testAddToClient()
boto3.DEFAULT_SESSION = None
testAddToResource()

print("""
===============================
All Tests finished successfully
===============================
""")
