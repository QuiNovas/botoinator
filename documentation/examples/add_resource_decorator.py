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

testAddToResource()
