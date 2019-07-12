from django.conf.urls import url
from userinfo import views

urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login_/$',views.login_,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^list/$',views.list,name='list'),
    url(r'^list1/$',views.list1,name='list1'),
    url(r'^list2/$',views.list2,name='list2'),
    url(r'^list3/$',views.list3,name='list3'),
    url(r'^list4/$',views.list4,name='list4'),
    url(r'^list5/$',views.list5,name='list5'),
    url(r'^detail/$',views.detail,name='detail'),
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^center/$',views.center,name='center'),
    url(r'^edit/$',views.edit,name='edit'),
    url(r'^add_cart/$',views.add_cart,name='add_cart'),
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^cart_price/$',views.cart_price,name='cart_price'),
    url(r'^cart_num/%',views.cart_num,name='cart_num'),
    url(r'^change_cart/$',views.change_cart,name='change_cart'),
    url(r'^delete_cart/$',views.delete_cart,name='delete_cart'),
    url(r'^change_status_cart/$',views.change_status_cart,name='change_status_cart'),
    url(r'^order_center/$',views.order_center,name='order_center')
]