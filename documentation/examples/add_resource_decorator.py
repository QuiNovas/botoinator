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

@mock_sqs
def testAddToResource():
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

  # Unregister the decorator
  s.unregister_resource_decorator('sqs', 'Queue', 'delete')

  # Create a client off of our original session
  sqs3 = boto3.Session().resource('sqs', region_name='us-east-1')
  sqs3.create_queue(QueueName='baz')
  queue3 = sqs3.Queue('baz')
  queue3.delete('baz')

  # Method should not be decorated
  assert not hasattr(queue2.delete, 'testValue')

testAddToResource()
