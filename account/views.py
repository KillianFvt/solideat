from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.utils import login_user
from api.models import Restaurant


@csrf_exempt
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
    username = data["email"]
    password = data["password"]

    # check if the username and password are provided
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)

    # log in the user
    response = login_user(username, password, request)

    return response


@api_view(['GET'])
def logout_account(request):
    """
    This view logs out the current user
    :param request: WSGI request object
    :return: Response object
    """

    # check if the user is authenticated
    if request.user.is_authenticated or request.user.is_anonymous:
        logout(request)
        return Response({"message": "logout success"}, status=200)
    else:
        return Response({"error": "No account to log out"})


@csrf_exempt
@api_view(['POST'])
def register_account(request):
    """
    This view registers a new user
    :param request: WSGI request object
    :return: Response object
    """
    logout(request)

    data = request.data

    # get the username and password from the request data
    username = data["email"]
    email = username
    password = data["password"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    is_restaurateur = data["is_restaurateur"]

    print('is_restaurateur:',  is_restaurateur)

    # avis
    if is_restaurateur == "true":
        is_restaurateur = True
    else:
        is_restaurateur = False

    # check if the username and password are provided
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)

    # check if the user already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=400)

    # create a new user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    if is_restaurateur:
        group = Group.objects.get(name='RestaurantOwners')
        group.user_set.add(user)
        group.save()

    #TODO enlever
    group = Group.objects.get(name='RestaurantOwners')
    print(group.user_set.all())

    user.save()

    # log in the user
    login_user(username, password, request)

    return Response({'message': 'User created successfully'})


@api_view(['GET'])
def get_current_user(request):
    """
    This view returns the current logged-in user
    :param request: WSGI request object
    :return: Response object
    """

    current_user = request.user
    ro_group = Group.objects.get(name='RestaurantOwners')
    is_restaurant_owner = current_user.groups.contains(ro_group)
    restaurant_id = None

    if is_restaurant_owner:
        restaurant_id = Restaurant.objects.filter(owner=current_user).first()

    # check if the user is authenticated
    if current_user.is_authenticated:
        return Response({
            'username': current_user.username,
            'id': current_user.id,
            'is_restaurant_owner': is_restaurant_owner,
            'restaurant': restaurant_id
        })
    else:
        return Response({'error': 'User is not authenticated'}, status=400)
