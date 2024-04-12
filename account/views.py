from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def login_account(request):
    """
    This view logs in a user
    :param request: WSGI request object
    :return: Response object
    """

    data = request.data
    print(data)

    # get the username and password from the request data
    username = data["username"]
    password = data["password"]

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


@api_view(['GET'])
def get_current_user(request):
    """
    This view returns the current logged-in user
    :param request: WSGI request object
    :return: Response object
    """

    # check if the user is authenticated
    if request.user.is_authenticated:
        return Response({'username': request.user.username})
    else:
        return Response({'message': 'User is not authenticated'}, status=400)