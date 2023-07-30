class CredentialsNotFound(Exception):
    """
    Error that occurs when the MongoDB
    URI is not found in the .env file
    """


class ClientError(Exception):
    """
    Error occurring when instantiating a MongoDB
    client probably due to a formatting
    error in the URI
    """

    pass


class DatabaseError(Exception):
    """
    Error that occurs when connecting to a MongoDB
    database probably because the credentials
    inside the URI are not correct
    """

    pass
