#!/usr/bin/env python3.7

import boto3
import botoinator
from moto import mock_s3
import time
import inspect
def myDecorator(value1, value2, value3):
  def test_decorator(func):
    func.testValue = (value1, value2, value3)
    print(value1)
    return func
  return test_decorator

@mock_s3
def testRegisterClient():
  s = boto3.session.Session()
  s.register_client_decorator('s3', 'create_bucket', myDecorator(time.time(), "string", True))
  client = s.client('s3')
  result = client.create_bucket
  assert isinstance(result.testValue[0], float) == 1 and result.testValue[1] == "string" and result.testValue[2] == True and isinstance(result.testValue, tuple)

@mock_s3
def testRegisterResource():
  s = boto3.session.Session()
  r = s.resource('s3')
  s.register_resource_decorator('s3', r, 'create_bucket', myDecorator(time.time(), "string", True))
  dir(s)
  result = r.create_bucket
  #print(result.testValue)
  #assert result.testValue[0] == 1 and result.testValue[1] == "string" and result.testValue[2] == True and isinstance(result.testValue, tuple)


#testRegisterClient()
testRegisterResource()
