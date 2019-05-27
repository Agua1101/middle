# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DCategory(models.Model):
    category = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=40, blank=True, null=True)
    book_counts = models.IntegerField(blank=True, null=True)
    category_pid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_category'


class DOrderiterm(models.Model):
    shop_id = models.IntegerField(primary_key=True)
    shop_bookid = models.IntegerField(blank=True, null=True)
    shop_ordid = models.IntegerField(blank=True, null=True)
    shop_num = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_orderiterm'


class TAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    detail_address = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    telphone = models.BigIntegerField(blank=True, null=True)
    addr_mobile = models.BigIntegerField(blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    less_address = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_address'


class TBook(models.Model):
    id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=100, blank=True, null=True)
    market_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dang_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sales_volume = models.IntegerField(blank=True, null=True)
    upload_date = models.CharField(max_length=40, blank=True, null=True)
    author = models.CharField(max_length=40, blank=True, null=True)
    press = models.CharField(max_length=40, blank=True, null=True)
    publish_date = models.CharField(max_length=40, blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    print_time = models.CharField(max_length=40, blank=True, null=True)
    num_print = models.CharField(max_length=40, blank=True, null=True)
    isbn = models.CharField(db_column='ISBN', max_length=40, blank=True, null=True)  # Field name made lowercase.
    w_num = models.CharField(max_length=40, blank=True, null=True)
    p_num = models.CharField(max_length=40, blank=True, null=True)
    format = models.CharField(max_length=40, blank=True, null=True)
    paper_type = models.CharField(max_length=40, blank=True, null=True)
    pack_type = models.CharField(max_length=40, blank=True, null=True)
    editor_choice = models.TextField(blank=True, null=True)
    content_abstract = models.TextField(blank=True, null=True)
    author_blurb = models.TextField(blank=True, null=True)
    t_index = models.TextField(blank=True, null=True)
    t_media = models.TextField(blank=True, null=True)
    t_illustration = models.TextField(blank=True, null=True)
    # book_category = models.ForeignKey(DCategory, models.DO_NOTHING, db_column='book_category', blank=True, null=True)
    book_category = models.IntegerField(blank=True, null=True)
    pic_path = models.TextField(blank=True, null=True)
    series_name = models.CharField(max_length=200, blank=True, null=True)
    customer_socre = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    book_status = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_book'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    num = models.CharField(max_length=200, blank=True, null=True)
    create_time = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_addrid = models.IntegerField(blank=True, null=True)
    order_uid = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order'


class TUser(models.Model):
    id = models.IntegerField(primary_key=True)
    t_name = models.CharField(max_length=20, blank=True, null=True)
    t_email = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'

class TOrder_ok(models.Model):
    t_code = models.CharField(max_length=200, null=True)
    t_userid = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_orderok'