=======================
apigatewaydisconnectapi
=======================

Provides a boto3 client class by the same name with a disconnect method for
disconnecting websocket clients.

The boto3 client for managing API Gateway connected websockets provides
a mechanism for posting data back to a client, but does not provide
a mechanism for forcing the disconnect of a client. It is left up to
the developer to build a signature version 4 authentication and
make the DELETE call themselves.

This package creates a boto3 client class called ``apigatewaydisconnectapi``
that supports disconnecting a client. The client object is created in the
same way that the ``apigatewaymanagementapi`` is created.

*class* **ApiGatewayDisconnectApi.Client**

  A low-level client representing ApiGatewayDisconnectApi

    .. code:: python

      import apigatewaydisconnectapi
      import boto3

      client = boto3.client('apigatewaydisconnectapi')

  **disconnect(**kwargs)**
    Disconnects the specified connection

    **Request Syntax**

      .. code:: python

        response = client.disconnect(
          ConnectionId='string'
        )

    **Parameters**

    * **ConnectionId** (string) --

      **[REQUIRED]**

      The identifier of the connection that a specific client is using.

    **Returns**

    None
