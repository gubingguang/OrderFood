from django.db import models

# Create your models here.
class Users(models.Model):
    uphone = models.CharField(max_length=20, verbose_name='电话号码')
    upwd = models.CharField(max_length=20, verbose_name='密码')
    uemail = models.EmailField(verbose_name='电子邮箱')
    uname = models.CharField(max_length=20, verbose_name='用户名')
    isActive = models.BooleanField(default=True, verbose_name='是否激活')

    def __str__(self):
        return self.uphone

    def to_dict(self):
        dic = {
            'id': self.id,
            'uphone': self.uphone,
            'upwd': self.upwd,
            'uname': self.uname,
            'uemail': self.uemail,
            'isActive': self.isActive
        }
        return dic

# 创建商品类型的实体 - GoodsType
class GoodsType(models.Model):
    # 商品类型名称
    title = models.CharField(max_length=50, verbose_name='商品类型名称')
    # 商品类型图片
    picture = models.ImageField(upload_to='static/upload/goodstype', null=True,
                                verbose_name='商品类型图片')
    # 商品类型描述
    desc = models.TextField(verbose_name='商品类型描述')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'GoodsType'
        verbose_name = '商品类型'
        verbose_name_plural = verbose_name

    def to_dict(self):
        dic = {
            'title': self.title,
            # __str__ (等同于tostring)解决 static/upload/goodstype/t4.png> is not JSON serializable
            'picture': self.picture.__str__(),
            'desc': self.desc,
        }
        return dic

# 创建商品实体 - Goods
class Goods(models.Model):
    # 商品名称
    title = models.CharField(max_length=40, verbose_name='商品名称')
    # 商品价格
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='商品价格')
    # 商品规格
    spec = models.CharField(max_length=30, verbose_name='商品规格')
    # 商品图片
    picture = models.ImageField(upload_to='static/upload/goods', null=True, verbose_name='商品图片')
    # 商品类型
    goodsType = models.ForeignKey(GoodsType, verbose_name='商品类型')
    # 是否上架
    isActive = models.BooleanField(default=True, verbose_name='是否上架')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

# 购物车表
class CartInfo(models.Model):
    # 属性: user, 外键,引用自Users实体
    user = models.ForeignKey(Users)
    # 属性: good, 外键,引用自Goods实体
    good = models.ForeignKey(Goods)
    # 属性: ccount, 整数,表示该商品的购买数量
    ccount = models.IntegerField()

    class Meta:
        db_table = 'CartInfo'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name



