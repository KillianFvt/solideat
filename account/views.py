from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def login(request):
    """
    This view logs in a user
    :param request: WSGI request object
    :return: Response object
    """

    # get the username and password from the request data
    username = request.data.get('username')
    password = request.data.get('password')

    # check if the username and password are provided
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)

    # authenticate the user
    user = authenticate(username=username, password=password)

    # check if the user is authenticated and valid
    if user is not None:
        login(request, user)  # log in the user
        request.session.save()  # not necessary, but it's a good practice to save the session
        return Response({'message': 'Login successful'})
    else:
        return Response({'message': 'Login failed'}, status=400)
