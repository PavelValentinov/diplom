from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from app.forms import UserRegistrationForm, LoginForm
from app.models import User, Product, ProductInfo, Category
from .serializers import UserSerializer, ProductSerializer, ProductInfoSerializer, CategorySerializer
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


# def products_view(request):
#     template_name = "products.html"
#     context = {}
#     product = Product.objects.all()
#     serializer = ProductSerializer(product, many=True)
#     print(product)
#     context['product'] = product
#     print(context)
#     return render(request, template_name, context)


class ProductApiView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ['name']

class CategoryApiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name']


# class ProductInfoApiView(ModelViewSet):
#     serializer_class = ProductInfoSerializer
#
#     search_fields = ['product__name', 'model']
#
#     def get_queryset(self):
#         query = Q(shop__state=True)
#
#         shop_id = self.request.GET.get('shop_id', None)
#         category_id = self.request.GET.get('category_id', None)
#
#         if shop_id:
#             query = query & Q(shop_id=shop_id)
#
#         if category_id:
#             query = query & Q(product__category_id=category_id)
#
#         queryset = ProductInfo.objects.filter(query).select_related(
#             'shop', 'product__category').prefetch_related(
#             'product_parameters__parameter').distinct()
#
#         return queryset



def products_detail_view(request, slug):
    template = 'product_detail.html'
    context = {}
    # product_info = ProductInfo.objects.filter(product_id=request.product.id)
    product = Product.objects.filter(slug=slug)
    context['product'] = product
    return render(request, template, context)

def register_view(request):
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

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Аутентификация прошла успешно')
                else:
                    return HttpResponse('Аккаунт заблокирован, пожалуйста, обратитесь к администратуру сайта ')
            else:
                return HttpResponse('Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})