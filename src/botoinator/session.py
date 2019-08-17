import boto3


class DecoratedSession(boto3.session.Session):


  __decorators = {}
  
  
  def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 aws_session_token=None, region_name=None,
                 botocore_session=None, profile_name=None):
    super().__init__(
      aws_access_key_id=aws_access_key_id,
      aws_secret_access_key=aws_secret_access_key,
      aws_session_token=aws_session_token,
      region_name=region_name,
      botocore_session=botocore_session,
      profile_name=profile_name
    )
    self.__decorators = {}
    for event_name, decorator_map in DecoratedSession.__decorators.items():
      for method_name, decorator in decorator_map.items():
        self.__register_decorator(event_name, method_name, decorator) 
    

  @classmethod
  def add_client_decorator(cls, client_name, method_names, decorator):
    """
    Add the decorator function to the class' statically registered decorators.

    Class-registered decorators will be applied to every DecoratedSession object created.

    Arguments:
    client_name -- the boto3 name of the client to apply the decorator to.
    method_names -- one or more method names of the client to apply the decorator to. Single names can be a string.
    decorator -- the decorator function. Must be a function that takes a function and returns a function. The returned function must take (*args, **kwargs) as arguments.
    """
    assert isinstance(method_names, (str, list, tuple, set)), 'method_names must be a string, list, tuple or set'
    event_name = 'creating-client-class.{}'.format(client_name)
    if isinstance(method_names, str):
      cls.__add_decorator(event_name, method_names, decorator)
    else:
      for method_name in method_names:
        assert isinstance(m, str), 'method {} must be a string'.format(method_name)
        cls.__add_decorator(event_name, method_name, decorator)


  @classmethod
  def add_resource_decorator(cls, service_name, resource_name, method_names, decorator):
    """
    Add the decorator function to the class' statically registered decorators.

    Class-registered decorators will be applied to every DecoratedSession object created.

    Arguments:
    service_name -- the boto3 name of the service to apply the decorator to.
    resource_name -- the boto3 name of the resource of the service to apply the decorator to.
    method_names -- one or more method names of the resource to apply the decorator to. Single names can be a string.
    decorator -- the decorator function. Must be a function that takes a function and returns a function. The returned function must take (*args, **kwargs) as arguments
    """
    assert isinstance(method_names, (str, list, tuple, set)), 'method_names must be a string, list, tuple or set'
    event_name = 'creating-resource-class.{}.{}'.format(service_name, resource_name)
    if isinstance(method_names, str):
      cls.__add_decorator(event_name, method_names, decorator)
    else:
      for method_name in method_names:
        assert isinstance(m, str), 'method_name {} must be a string'.format(method_name)
        cls.__add_decorator(event_name, method_name, decorator)


  def register_client_decorator(self, client_name, method_names, decorator):
    """
    Add the decorator function to the session's registered decorators.

    Arguments:
    client_name -- the boto3 name of the client to apply the decorator to.
    method_names -- one or more method names of the client to apply the decorator to. Single names can be a string.
    decorator -- the decorator function. Must be a function that takes a function and returns a function. The returned function must take (*args, **kwargs) as arguments.
    """
    assert isinstance(method_names, (str, list, tuple, set)), 'method_names must be a string, list, tuple or set'
    event_name = 'creating-client-class.{}'.format(client_name)
    if isinstance(method_names, str):
      self.__register_decorator(event_name, method_names, decorator)
    else:
      for method_name in method_names:
        assert isinstance(m, str), 'method_name {} must be a string'.format(m)
        self.__register_decorator(event_name, method_name, decorator)



  def register_resource_decorator(self, service_name, resource_name, method_names, decorator):
    """
    Add the decorator function to the session's statically registered decorators.

    Arguments:
    service_name -- the boto3 name of the service to apply the decorator to.
    resource_name -- the boto3 name of the resource of the service to apply the decorator to.
    method_names -- one or more method names of the resource to apply the decorator to. Single names can be a string.
    decorator -- the decorator function. Must be a function that takes a function and returns a function. The returned function must take (*args, **kwargs) as arguments
    """
    assert isinstance(method_names, (str, list, tuple, set)), 'method_names must be a string, list, tuple or set'
    event_name = 'creating-resource-class.{}.{}'.format(service_name, resource_name)
    if isinstance(method_names, str):
      self.__register_decorator(event_name, method_names, decorator)
    else:
      for method_name in method_names:
        assert isinstance(m, str), 'method_name {} must be a string'.format(method_name)
        self.__register_decorator(event_name, method_name, decorator)


  @classmethod
  def remove_client_decorator(cls, client_name, method_names):
    """
    Removes the decorator function from the class' statically registered decorators.

    Class-registered decorators will be applied to every DecoratedSession object created.

    Arguments:
    client_name -- the boto3 name of the client to apply the decorator to.
    method_names -- one or more method names of the client to apply the decorator to. Single names can be a string.
    """
    assert isinstance(method_names, (str, list, tuple, set, None)), 'method_names must be a string, list, tuple, set or None'
    event_name = 'creating-client-class.{}'.format(client_name)
    if not method_names or isinstance(method_names, str):
      cls.__remove_decorator(event_name, method_names)
    else:
      for method_name in method_names:
        assert isinstance(method_name, str), 'method_name {} must be a string'.format(m)
        cls.__remove_decorator(event_name, method_name)
    


  @classmethod
  def remove_resource_decorator(cls, service_name, resource_name, method_names):
    """
    Removes the decorator function from the class' statically registered decorators.

    Class-registered decorators will be applied to every DecoratedSession object created.

    Arguments:
    service_name -- the boto3 name of the service to apply the decorator to.
    resource_name -- the boto3 name of the resource of the service to apply the decorator to.
    method_names -- one or more method names of the resource to apply the decorator to. Single names can be a string.
    """
    assert isinstance(method_names, (str, list, tuple, set, None)), 'method_names must be a string, list, tuple, set or None'
    event_name = 'creating-resource-class.{}.{}'.format(service_name, resource_name)
    if not method_names or isinstance(method_names, str):
      cls.__remove_decorator(event_name, method_names)
    else:
      for method_name in method_names:
        cls.__remove_decorator(event_name, method_name)


  def unregister_client_decorator(self, client_name, method_names):
    """
    Removes the decorator function from the session's registered decorators.

    Arguments:
    client_name -- the boto3 name of the client to apply the decorator to.
    method_names -- one or more method names of the client to apply the decorator to. Single names can be a string.
    """
    assert isinstance(method_names, (str, list, tuple, set, None)), 'method_names must be a string, list, tuple, set or None'
    event_name = 'creating-client-class.{}'.format(client_name)
    if not method_names or isinstance(method_names, str):
      self.__unregister_decorator(event_name, method_names)
    else:
      for method_name in method_names:
        self.__unregister_decorator(event_name, method_name)


  def unregister_resource_decorator(self, service_name, resource_name, method_names):
    """
    Removes the decorator function from the session's registered decorators.

    Arguments:
    service_name -- the boto3 name of the service to apply the decorator to.
    resource_name -- the boto3 name of the resource of the service to apply the decorator to.
    method_names -- one or more method names of the resource to apply the decorator to. Single names can be a string.
    """
    assert isinstance(method_names, (str, list, tuple, set, None)), 'method_names must be a string, list, tuple, set or None'
    event_name = 'creating-resource-class.{}.{}'.format(service_name, resource_name)
    if not method_names or isinstance(method_names, str):
      self.__unregister_decorator(event_name, method_names)
    else:
      for method_name in method_names:
        self.__unregister_decorator(event_name'creating-resource-class.{}.{}'.format(service, resource), method_name)

  
  @classmethod
  def __add_decorator(cls, event_name, method_name, decorator):
    assert callable(decorator), 'decorator must be a function'
    decorator_map = cls.__decorators.get(event_name)
    if not decorator_map:
      decorator_map = {}
      cls.__decorators[event_name] = decorator_map
    decorator_map[method_name] = decorator


  def __decorate(self, event_name, class_attributes, **kwargs):
    decorator_map = self.__decorators.get(event_name)
    if decorator_map:
      for method_name, decorator in decorator_map.items():
        if method_name in class_attributes:
          class_attributes[method_name] = decorator(class_attributes[method_name])


  def __register_decorator(self, event_name, method_name, decorator):
    assert callable(decorator), 'decorator must be a function'
    decorator_map = self.__decorators.get(event_name)
    if not decorator_map:
      decorator_map = {}
      self.__decorators[event_name] = decorator_map
      self.events.register(event_name, self.__decorate)
    decorator_map[method_name] = decorator


  @classmethod
  def __remove_decorator(cls, event_name, method_name):
    decorator_map = cls.__decorators.get(event_name)
    if decorator_map and method_name:
      decorator_map.pop(method_name)
    if not decorator_map or not method_name:
      cls.__decorators.pop(event_name)


  def __unregister_decorator(self, event_name, method_name):
    decorator_map = self.__decorators.get(event_name)
    if decorator_map and method_name:
      decorator_map.pop(method_name)
    if not decorator_map or not method_name:
      self.__decorators.pop(event_name)
      self.events.unregister(event_name)
