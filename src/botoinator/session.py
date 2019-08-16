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
      for method, decorator in decorator_map.items():
        self.__register_decorator(event_name, method, decorator) 
    

  @classmethod
  def add_client_decorator(cls, client, method, decorator):
    cls.__add_decorator('creating-client-class.{}'.format(client), method, decorator)


  @classmethod
  def add_resource_decorator(cls, service, resource, method, decorator):
    cls.__add_decorator('creating-resource-class.{}.{}'.format(service, resource), method, decorator)


  def register_client_decorator(self, client, method, decorator):
    self.__register_decorator('creating-client-class.{}'.format(client), method, decorator)


  def register_resource_decorator(self, service, resource, method, decorator):
    self.__register_decorator('creating-resource-class.{}.{}'.format(service, resource), method, decorator)


  @classmethod
  def remove_client_decorator(cls, client, method):
    cls.__remove_decorator(client, method)


  @classmethod
  def remove_resource_decorator(cls, service, resource, method):
    cls.__remove_decorator('{}.{}'.format(service, resource), method)


  def unregister_client_decorator(self, client, method):
    self.__unregister_decorator('creating-client-class.{}'.format(client), method)


  def unregister_resource_decorator(self, service, resource, method):
    self.__unregister_decorator('creating-resource-class.{}.{}'.format(service, resource), method)

  
  @classmethod
  def __add_decorator(cls, class_name, method, decorator):
    assert callable(decorator), 'decorator must be a function'
    decorator_map = cls.__decorators.get(class_name)
    if not decorator_map:
      decorator_map = {}
      cls.__decorators[class_name] = decorator_map
    decorator_map[method] = decorator


  def __decorate(self, event_name, class_attributes, **kwargs):
    decorator_map = self.__decorators.get(event_name)
    if decorator_map:
      for method, decorator in decorator_map.items():
        if method in class_attributes:
          class_attributes[method] = decorator(class_attributes[method])


  def __register_decorator(self, event_name, method, decorator):
    assert callable(decorator), 'decorator must be a function'
    decorator_map = self.__decorators.get(event_name)
    if not decorator_map:
      decorator_map = {}
      self.__decorators[event_name] = decorator_map
      self.events.register(event_name, self.__decorate)
    decorator_map[method] = decorator


  @classmethod
  def __remove_decorator(cls, class_name, method):
    decorator_map = cls.__decorators.get(class_name)
    if decorator_map:
      decorator_map.pop(method)
    if not decorator_map:
      cls.__decorators.pop(class_name)


  def __unregister_decorator(self, event_name, method):
    decorator_map = self.__decorators.get(event_name)
    if decorator_map:
      decorator_map.pop(method)
    if not decorator_map:
      self.__decorators.pop(event_name)
      self.events.unregister(event_name)
