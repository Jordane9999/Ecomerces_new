from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from Stors.models import Cart, GroupeProduct, Order, Product
from .form import ProductForm
from django.core.paginator import Paginator
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.http import JsonResponse



# Create pdf module
# importing the necessary libraries
from io import BytesIO 



# Create your views here.

# class indexhome(ListView):
#     model = Product
#     template_name = "Stors/Acceuil.html"
#     products = ''
#     messages = ''
    
#     def get_context_data(request,*args, **kwargs):
        
#         categories = GroupeProduct.objects.all()
#         context =  {

#             'categories':categories,
#         }
#         return context
    
#     def get(self, request,*args, **kwargs):
#         if request.method == 'GET':
#             name = request.GET.get('search')
#             if name is not None:
#                 products = Product.objects.filter(name__icontains=name)
#                 if bool(products):
#                     products = Product.objects.filter(name__icontains=name)
#                 else:
#                     messages = "Le prosuits rechercher n'existe pas pardons chercher un produit valide" 

#         context = super().get_context_data(**kwargs) 
#         context =  {            
#             'products':products,
#             'name':name,
#             'messages':messages,
#             # 'produit':produit
#         }
#         return context
    
    
def index(request):  
   
    categories = GroupeProduct.objects.all()
    #produit = Product.objects.all()
    products_friperies  = ''
    products_vehicule = ''
    products_electronic = ''
    products_other = ''
    
    category_name_friperies = ''
    category_name_vehicule = ''
    category_name_electronic = ''
    category_name_other = ''
    for e in categories:
        print(e.name)
        item_name = request.GET.get('search')
        if e.name == "FRIPERIES":
                products_friperies = Product.objects.filter(groupe__name__contains="FRIPERIES")
                paginator = Paginator(products_friperies, 8)
                page = request.GET.get('page')
                products_friperies = paginator.get_page(page)
                category_name_friperies = e.name
                print(category_name_friperies)
                print(products_friperies)
        if e.name == "VEHICULE":
                products_vehicule = Product.objects.filter(groupe__name__contains="VEHICULE")
                paginator = Paginator(products_vehicule, 8)
                page = request.GET.get('page')
                products_vehicule = paginator.get_page(page)
                category_name_vehicule = e.name
                print(products_vehicule)
        if e.name == "ELECTRONIC":
            products_electronic = Product.objects.filter(groupe__name__contains="ELECTRONIC")
            paginator = Paginator(products_electronic, 8)
            page = request.GET.get('page')
            products_electronic = paginator.get_page(page)
            category_name_electronic = e.name
            print(products_electronic)
        if e.name == "OTHER":
            products_other = Product.objects.filter(groupe__name__contains="OTHER")
            paginator = Paginator(products_other, 8)
            page = request.GET.get('page')
            products_other = paginator.get_page(page)
            category_name_other = e.name
            print(products_other)           

               
    #pagination = categories.product_set.all()
    products = ''
    messages = ''
    
    if request.method == 'GET':
        name = request.GET.get('search')
        if name is not None:
            products = Product.objects.filter(name__icontains=name)
            if bool(products):
                products = Product.objects.filter(name__icontains=name)
            else:
                messages = "Le prosuits rechercher n'existe pas pardons chercher un produit valide" 
    

    context =  {

        'categories':categories,
        'products':products,
        'name':name,
        'messages':messages,
        #Le nom des Category de produits
        'name_friperies':category_name_friperies,
        'name_vehicule':category_name_vehicule,
        'name_electronic':category_name_electronic,
        'name_other':category_name_other,
        #Parcourir les produits dans le templates
        'friperies': products_friperies,
        'vehicule':products_vehicule,
        'electronic':products_electronic,
        'other':products_other,
        
    }
    return render(request, 'Stors/Acceuil.html', context)


#Une fonction qui me permet de recuperer les données
def getdata(request):
    categories = GroupeProduct.objects.all()
    produit = Product.objects.all()
    ordre = Order.objects.all()
    panier = Cart.objects.all()
    context = {
        'categories': list(categories.values()),
        'produit': list(produit.values()),
        'ordre': list(ordre.values()),
        'panier': list(panier.values())
    }

    return JsonResponse(context)


#La vue en detail
def Product_detail(request, pk):
    products = get_object_or_404(Product, pk=pk)
    categories = GroupeProduct.objects.all()
    context ={
        'product':products,
        'categories':categories
    }
    return render(request, "Stors/detail.html", context)


def category_product(request, pk):
    category = get_object_or_404(GroupeProduct, pk=pk)
    categories = GroupeProduct.objects.all()
    products = category.product_set.all()


    if request.method == 'GET':
        name = request.GET.get('search')
        if name is not None:
            products = category.product_set.filter(name__icontains=name)

    context =  {

        'categories':categories,
        'products' : products,
        'category':category
    }
    return render(request, "Stors/category.html",context)


def add_to_cart(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)

    if created:
        cart.orders.add(order)
        cart.save()

    else:
        order.quantity += 1
        order.save()
       
    return redirect(reverse("detail", kwargs={"pk":pk}))

def panier_info(request):
    categories = GroupeProduct.objects.all()
    context = {
        'categories':categories
    }
    return render(request, "Stors/panier_info.html", context)

def panier_vide(request):
    categories = GroupeProduct.objects.all()
    context = {
        'categories':categories
    }
    return render(request, "Stors/panier_vide.html", context)


def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    categories = GroupeProduct.objects.all()
    if request.method == "GET":
        name = request.GET.get("search")

        if name is not None:
            cart = Product.objects.filter(name__icontains=name)

    return render(request, "Stors/panier.html", context={"orders":cart.orders.all(),'categories':categories})


def delete_cart(request):
    cart = request.user.cart

    if cart:
        cart.orders.all().delete()
        cart.delete()

    # if cart:= request.user.cart:
    #     cart.delete()

    return redirect("home")

def commande_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    categories = GroupeProduct.objects.all()
    orders= cart.orders.all()
    
    
    if request.method == 'GET':
        number = request.GET.get('numero')
        print(number)
        # User.number=number
        # print(User.number)
        
            
    productstotal = 0
    for order in orders:
        productstotal += (order.quantity * order.product.price)
    
    context={
        #"products":products,
        "orders":cart.orders.all(),
        'categories':categories,
        'total':productstotal
        }
    
    
    return render(request, "Stors/liste_commande.html", context)




# defining the function to convert an HTML file to a PDF file

# def html_to_pdf(template_src, context_dict={}):
#      template = get_template(template_src)
#      html  = template.render(context_dict)
#      result = BytesIO()
#      pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#      if not pdf.err:
#          return HttpResponse(result.getvalue(), content_type='application/pdf')
#      return None



def recus_pdf(request):
    cart = get_object_or_404(Cart, user=request.user)
    user = request.user
    categories = GroupeProduct.objects.all()
    orders= cart.orders.all()
    productstotal = 0
    for order in orders:
        productstotal += (order.quantity * order.product.price)
        
    # template = get_template('Stors/commande.html')
    
    context={
        #"products":products,
        "orders":cart.orders.all(),
        'categories':categories,
        'total':productstotal,
        'user':user
    }
    
    #html = template.render(context)
    
    html = html_to_pdf('Stors/commande.html', context)
    
    pdf = HttpResponse(html, content_type='application/pdf')
    
    return pdf 
    # return render(request, "Stors/commande.html", context)
    
    
    



##---------------------Creations des actions Administrateur---------------------------------------##

def Administrations(request):
    product = Product.objects.all()
    categories = GroupeProduct.objects.all()
    
    if request.method == 'GET':
        name = request.GET.get('search')
        if name is not None:
            product = Product.objects.filter(name__icontains=name)
    
    context = {
        'products':product,
        'categories':categories
    }
    return render(request, "Stors/Administrateur_page.html", context)

# class ProductCreateView(CreateView):
#     form_class = ProductForm
#     template_name = "Stors/add_product.html"
#     queryset = Product.objects.all()
#     success_url = "/"
    
#     #Verrifier que le formulaire est valide
#     def form_valid(self, form) :
#         print(form.cleaned_data)
#         return super().form_valid(form)
    
def ProductCreate(request):
    form = ProductForm(request.POST or None)
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist("thumbnail")
        print(data)
        print(images)
        category = GroupeProduct.objects.get(id=data['groupe'])
        prix = data['price']
        print(prix)
        stock=data['stock']
        for image in images:
          products = Product.objects.create(name = data['name'],groupe = category ,price = prix,stock = stock ,description = ['description'],thumbnail = image)
        # if form.is_valid():
        #     form.save()
            
        #     #pour rendre le formulaire vide sur le plant visuel
        #     #form = ProductForm()
        return redirect('home')
    return render(request, "Stors/add_product.html", {'form':form})
    
    
class ProductUpdateView(UpdateView):
    model = Product
    queryset = Product.objects.all()
    template_name = "Stors/update_product.html"
    context_object_name = "stors"
    fields = "__all__"
    
    
class ProductDeleteView(DeleteView):
    template_name = "Stors/delet_product.html"
    queryset = Product.objects.all()
    context_object_name = "stors"
    success_url = "/"
    
    
def contact(request):
    categories = GroupeProduct.objects.all()
    context = {
        'categories':categories
    }
    return render(request, "Stors/contact.html", context)


def about(request):
    categories = GroupeProduct.objects.all()
    
    context = {
        'categories':categories,        
    }
    return render(request, "Stors/about.html", context)
    