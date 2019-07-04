from django.db import models

# Create your models here.


from Mall.settings import ORDERSTATUS

# 用户信息
class UserInfo(models.Model):
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=30,null=True)
    phone = models.CharField(max_length=11,null=True)
    sex = models.BooleanField(default=0)
    regtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = 'userinfo'


# 收获地址
class Address(models.Model):
    aname = models.CharField(max_length=50)
    ads = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    postcode = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.aname
    class Meta:
        db_table = 'address'


# 商品分类表
class GoodsType(models.Model):
    # 分类名称
    title = models.CharField(max_length=30)
    # 简介
    desc = models.CharField(max_length=300)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'goodstype'

# 商品表
class Goods(models.Model):
    title = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    desc = models.CharField(max_length=300)
    details = models.CharField(max_length=500)
    commments = models.CharField(max_length=500)
    picture = models.ImageField(upload_to='static/image',default='xm5-80.jpg')
    type = models.ForeignKey(GoodsType,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'goods'

# 购物车表
class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo,db_column='user_id')
    good = models.ForeignKey(Goods,db_column='good_id')
    count = models.IntegerField(db_column='cart_count')

    def __str__(self):
        return self.user
    class Meta:
        db_table = 'cartinfo'

# 订单表
# 订单号orderNo
# 订单详情　orderdetails # 商品 数量　单价　描述
# 用户user 关联
# 地址address
# 收件人 adsname
# 收件电话　adsphone
# 下单时间　time
# 订单总数　total
# 订单总价　acount
# 订单状态　orderstatus

class Order(models.Model):
    orderNo = models.CharField(max_length=50)
    orderdetails = models.TextField()
    address = models.CharField(max_length=50)
    adsname = models.CharField(max_length=30)
    adsphone = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()
    acount = models.DecimalField(max_digits=8,decimal_places=2)
    orderstatus = models.IntegerField(choices=ORDERSTATUS,default=0)
    user = models.ForeignKey(UserInfo)

    def __str__(self):
        return self.orderNo
    class Meta:
        db_table = 'order'