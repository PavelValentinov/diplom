from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from app.forms import UserRegistrationForm
from app.models import User, Product
from app.serializers import UserSerializer


# class UserView(APIView):
#     def get(self, request, *args, **kwargs):
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)

def home_view(request):
    template_name = "index.html"
    context = {}

    product = Product.objects.all()
    context['product'] = product
    return render(request, template_name, context)

def users_view(request):
    template_name = "users.html"
    context = {}

    user = User.objects.all()
    context['user'] = user
    return render(request, template_name, context)

def products_view(request):
    template_name = "products.html"
    context = {}

    product = Product.objects.all()
    context['product'] = product
    return render(request, template_name, context)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})