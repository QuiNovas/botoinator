# Botoinator

### A python module that allows for declaring decorators to be added to boto3 methods


## Overview
  Botoinator allows you to apply decorators to boto3 methods on either a class or object level. It works through boto3 sessions to allow you to apply decorators to either all clients/resources of a particular session, or to specific clients/resources of boto3.DEFAULT_SESSION.

## Generated documentation
You can see the pydoc generated documentation [HERE](https://github.com/QuiNovas/botoinator/tree/master/documentation/botoinator.txt)

# Usage
### Decorate a method belonging to a client object to a single session
```python
session = boto3.session.Session()
session.register_client_decorator(service_name, method_names, decorator)
```
Arguments:
* service_name -- the boto3 name (as a string) of the client to apply the decorator to.
* method_names -- one or more method names of the client to apply the decorator to. Single names can be a string, while multiple names can be a list/tuple/set.
* decorator -- the decorator function. Must be a function that takes a function and returns a function. The returned function must take (*args, **kwargs) as arguments.

### Decorate a method belonging to a resource object in a single session
```python
session = boto3.session.Session()
session.register_resource_decorator(service_name, resource_name, method_names, decorator)
```
Arguments:
* service_name -- the boto3 name (as a string) of the service to apply the decorator to.
* resource_name -- the boto3 name of the resource of the service to apply the decorator to.
* method_names -- one or more method names of the resource to apply the decorator to. Single names can be a string, while multiple names should be a list/tuple/set.
* decorator -- the decorator function. Must be a function that takes a function and returns a function. The returned function must take (*args, **kwargs) as arguments

### Decorate a method for clients created in any session
```python
boto3.session.Session.add_client_decorator(service_name, method_names, decorator)
```
Arguments:
* service_name -- the boto3 name (as a string) of the client to apply the decorator to.
* method_names -- one or more method names of the client to apply the decorator to. Single names can be a string, while multiple names should be a list/tuple/set.
* decorator -- the decorator function. Must be a function that takes a function and returns a function. The returned function must take (*args, **kwargs) as arguments.

### Decorate a method of a resource in all sessions
```python
boto3.session.Session.add_resource_decorator(service_name, resource_name, method_names, decorator)
```
Arguments:
* service_name -- the boto3 name of the service to apply the decorator to.
* resource_name -- the boto3 name of the resource of the service to apply the decorator to.
* method_names -- one or more method names of the resource to apply the decorator to. Single names can be a string, while multiple names should be a list/tuple/set
* decorator -- the decorator function. Must be a function that takes a function and returns a function. The returned function must take (*args, **kwargs) as arguments

### Unregister a decorator so that future clients will not have their methods decorated. Clients that have already registered decorators to methods will retain their decoration.
```python
session = boto3.session.Session()
session.unregister_client_decorator(service_name, method_names)
```
Arguments:
* service_name -- the boto3 name of the service to apply the decorator to.
* method_names -- one or more method names of the client to apply the decorator to. Single names can be a string, while multiple names should be a list/tuple/set

### Unregister a decorator so that future resources will not have their methods decorated. Resources that have already registered decorators to methods will retain their decoration.
```python
session = boto3.session.Session()
session.unregister_resource_decorator(service_name, resource_name, method_names)
```
Arguments:
* service_name -- the boto3 name of the service to apply the decorator to.
* resource_name -- the boto3 name of the resource of the service to apply the decorator to.
* method_names -- one or more method names of the resource to apply the decorator to. Single names can be a string, while multiple names should be a list/tuple/set

### Undecorate a method for clients created in any session.
```python
boto3.session.Session.remove_client_decorator(service_name, method_names)
```
Arguments:
* service_name -- the boto3 name (as a string) of the client to apply the decorator to.
* method_names -- one or more method names of the client to apply the decorator to. Single names can be a string, while multiple names should be a list/tuple/set.

### Undecorate a method of a resource in all sessions
```python
boto3.session.Session.remove_resource_decorator(service_name, resource_name, method_names)
```
Arguments:
* service_name -- the boto3 name of the service to apply the decorator to.
* resource_name -- the boto3 name of the resource of the service to apply the decorator to.
* method_names -- one or more method names of the resource to apply the decorator to. Single names can be a string, while multiple names should be a list/tuple/set

# boto3 convienence methods
If you use the ```boto3.client()``` or ```boto3.resource()``` methods, these create a default session object found at ```boto3.DEFAULT_SESSION```.
Changing the default session's decorators requires using the ```register_xxx``` and ```unregister_xxx``` methods documented here.
For example ```boto3.DEFAULT_SESSION.register_client_decorator(...)```.

## Example of decorating create_bucket() on a single boto3 session
```python
import boto3
import botoinator
from moto import mock_s3, mock_sqs

""" This is our decorator that we will apply to boto3 methods """
def myDecorator(func):
  def test_decorator(*args, **kwargs):
    setattr(test_decorator, 'testValue', True) # Add this attribute to the returned function for testing
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
```

#### View [more examples in the project documentation directory](https://github.com/QuiNovas/botoinator/tree/master/documentation/examples).
