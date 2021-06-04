from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.conf.urls.static import static

from books import views
from book_store import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('reg/', views.reg, name='reg'),
    path('regack/', views.reg_ack, name='regack'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search,name='search'),
    url(r'^cate/(?P<prod_id>[0-9]+)', views.cate, name='cate'),
    url(r'^sprod/(?P<prod_id>[0-9]+)', views.sprod, name='sprod'),

    #---------------- Provider ------------------

    path('procategory',views.pro_category,name='procategory'),
    url(r'^pro_cate/(?P<prod_id>[0-9]+)', views.pro_category_items, name='pro_category_items'),
    path('prohome/',views.pro_home,name='pro_home'),
    path('proaddbook/', views.pro_add_book, name='pro_add_book'),
    path('prodelbook/', views.pro_del_book, name='pro_del_book'),
    path('proreport/',views.pro_report,name='pro_report'),
    path('proaddcate/',views.pro_add_cate,name='pro_add_cate'),
    path('prodelcate/',views.pro_del_cate,name='pro_del_cate'),

    # ---------------- Customer ------------------

    path('cart0/', views.cart0, name='cart0'),
    path('cart/', views.cart, name='cart'),
    path('cartconfirm/', views.cartconfirm, name='cartconfirm'),
    path('orders/', views.orders, name='orders'),
    path('account/', views.account, name='account'),
    path('forgot/', views.forgot, name='forgot'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
