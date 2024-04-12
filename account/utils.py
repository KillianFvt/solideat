from django.contrib.auth import authenticate, login
from rest_framework.response import Response


def login_user(username: str, password: str, request) -> Response:
    # authenticate the user
    user = authenticate(username=username, password=password)

    # check if the user is authenticated and valid
    if user is not None:
        login(request, user)  # log in the user
        request.session.save()  # not necessary, but it's a good practice to save the session
        return Response({'message': 'Login successful'})
    else:
        return Response({'message': 'Login failed'}, status=400)