from django.db import models

class Users(models.Model):
    first_name = models.CharField(max_length=20)
    second_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    user_mail = models.EmailField()
    user_password = models.CharField(max_length=20)
    user_number = models.CharField(max_length=10)
    user_address = models.TextField()
    user_role = models.CharField(max_length=10, default='costumer')

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name_plural = 'Users'

class Books(models.Model):
    book_title = models.CharField(max_length=100)
    book_provider_mail = models.EmailField()
    book_isbn10 = models.CharField(max_length=10)
    book_author = models.CharField(max_length=20)
    book_publisher = models.CharField(max_length=20)
    book_copies = models.IntegerField()
    book_price = models.IntegerField()
    book_description = models.TextField()
    book_language = models.CharField(max_length=20)
    book_year = models.CharField(max_length=4)
    book_image = models.ImageField(upload_to='', blank=True)
    book_category = models.TextField(max_length=50)
    book_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.book_title
    class Meta:
        verbose_name_plural = 'Books'

class Categories(models.Model):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='')
    category_status = models.CharField(max_length=20,default='on')

    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name_plural = 'Categories'

class Book_comments(models.Model):
    book_title = models.CharField(max_length=100)
    book_user_mail = models.EmailField(blank=True, null=True)
    book_comment = models.TextField()

    def __str__(self):
        return self.book_title
    class Meta:
        verbose_name_plural = 'Book_comments'

class Rating(models.Model):
    user_mail = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    rating_value = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Rating'

class Cart(models.Model):
    book_id = models.IntegerField()
    book_title = models.CharField(max_length=100)
    mail = models.EmailField()
    items = models.IntegerField(default=1)
    cost = models.IntegerField(default=0)
    status = models.CharField(default='no', max_length=3)

    def __str__(self):
        return self.book_title

    class Meta:
        verbose_name_plural = 'Cart'

class Card_details(models.Model):
    card_mail = models.EmailField()
    card_name = models.CharField(max_length=10,default='')
    card_number = models.CharField(max_length=10,default='')
    card_cvv = models.CharField(max_length=3,default='')

    def __str__(self):
        return self.card_mail

    class Meta:
        verbose_name_plural = 'Card_details'

class Orders(models.Model):
    order_mail = models.EmailField(default='')
    order_title = models.CharField(max_length=100)
    order_provider_mail = models.EmailField()
    order_isbn10 = models.CharField(max_length=10)
    order_author = models.CharField(max_length=20)
    order_publisher = models.CharField(max_length=20)
    order_copies = models.IntegerField()
    order_price = models.IntegerField()
    order_description = models.TextField()
    order_language = models.CharField(max_length=20)
    order_year = models.CharField(max_length=4)
    order_image = models.ImageField(upload_to='', blank=True)
    order_category = models.TextField(max_length=50)
    order_rating = models.FloatField(default=0.0)
    order_status = models.CharField(default='on', max_length=3)

    def __str__(self):
        return self.order_title
    class Meta:
        verbose_name_plural = 'Orders'
