from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from books.models import *

import os
from book_store import settings

def index(request):
    template = loader.get_template('index.html')
    context = {'tfmess': 'False'}
    context['cateobj'] = cateobj = Categories.objects.order_by('category_name')
    context['bobj'] = bobj = Books.objects.all()
    context['robj'] = robj = Rating.objects.all()

    c, t = 0, 0
    for b in bobj:
        c, t = 0, 0
        for r in robj:
            if b.book_title == r.title:
                c += int(r.rating_value)
        t = float(c / 5)
        b.book_rating = float(t)
        b.save()

    if request.session.has_key('user_mail'):
        context['user_mail'] = user_mail = request.session['user_mail']
        context['tfmess'] = 'True'

    return HttpResponse(template.render(context,request))

def login(request):
    template = loader.get_template('login.html')
    context = {'tfmess': 'False'}
    request.session.flush()

    if request.session.has_key('user_mail'):
        context['user_mail'] = user_mail = request.session['user_mail']
        context['tfmess'] = 'True'

    if request.method == 'POST':

        user_mail = request.POST.get('uemail')
        user_password = request.POST.get('user_password')

        for x in Users.objects.all():
            if x.user_mail == user_mail and x.user_password == user_password:

                request.session['user_mail'] = user_mail

                if x.user_role == 'customer':

                    return redirect('index')

                if x.user_role == 'provider':
                    return redirect('procategory')

        context['message'] = "Permission denied, Incorrect Details"

    return HttpResponse(template.render(context,request))

def reg(request):
    template = loader.get_template('register.html')
    context = {'mess': '', 'tfmess': 'False'}
    request.session.flush()

    if request.session.has_key('user_mail'):
        context['user_mail'] = user_mail = request.session['user_mail']
        context['tfmess'] = 'True'

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_mail = request.POST.get('user_mail')
        user_password = request.POST.get('user_password')
        user_password1 = request.POST.get('user_password1')
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        user_address = request.POST.get('user_address')
        user_number = request.POST.get('user_number')

        user_role = 'customer'

        if user_password != user_password1:
            context['mess'] = 'Password Mismatch'

        try:
            if len(user_number) != 10:
                context['mess'] = 'Enter Proper Phone Number'
            user_number = int(user_number)
        except:
            context['mess'] = 'Enter Proper Phone Number'


        if context['mess'] == '':
            for x in Users.objects.all():
                if x.user_mail == user_mail:
                    context['mess'] = 'mail id is already registered'

            if context['mess'] != 'mail id is already registered':
                ucobj = Users.objects.create(
                    user_name=user_name,
                    user_mail=user_mail,
                    user_password=user_password,
                    first_name=first_name,
                    second_name=second_name,
                    user_address=user_address,
                    user_number=user_number,
                    user_role=user_role
                )
                ucobj.save()
                cardobj = Card_details.objects.create(
                    card_mail=user_mail
                )
                cardobj.save()
                context['mess'] = 'Registration Successful'
                return redirect('regack')

    return HttpResponse(template.render(context,request))

def reg_ack(request):
    template = loader.get_template('registration_acknowledgement.html')
    context = {'mess': '', 'tfmess': 'False'}
    return HttpResponse(template.render(context, request))

def search(request):
    template = loader.get_template('search.html')
    context = {'mess': "",'tfmess': 'False'}
    nnn = ''
    if request.session.has_key('user_mail'):
        context['user_mail'] = user_mail = request.session['user_mail']
        context['tfmess'] = 'True'

    context['cobj'] = cobj = Categories.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    if request.method == 'POST':

        context['sval'] = sval = (request.POST.get('sval')).title()

        if sval == '':
            return redirect('index')

        for x in bobj:
            if x.book_author == sval or x.book_category == sval or x.book_title == sval or x.book_publisher == sval:
                nnn = 'True'

        if nnn == '':
            context['mess'] = 'Results not found'

    return HttpResponse(template.render(context, request))

def cate(request, prod_id):
    template = loader.get_template('cate.html')
    context = {'mess': "",'tfmess': 'False'}
    val = 0

    if request.session.has_key('user_mail'):
        context['user_mail'] = user_mail = request.session['user_mail']
        context['tfmess'] = 'True'

    context['cn'] = cn = Categories.objects.get(id=prod_id)

    context['cobj'] = cobj = Categories.objects.order_by('category_name')
    context['bobj'] = bobj = Books.objects.all()

    for x in bobj:
        if x.book_category == cn.category_name:
            val = 1

    if val == 0:
        context['mess'] = 'No books Available'

    return HttpResponse(template.render(context, request))

def sprod(request, prod_id):
    template = loader.get_template('singleproduct.html')
    context = {'mess': "single",'tfmess': 'False'}
    request.session['bid'] = None
    count = []

    if request.session.has_key('user_mail'):

        context['user_mail'] = user_mail = request.session['user_mail']
        context['tfmess'] = 'True'

        context['cn'] = cn = Books.objects.get(id=prod_id)
        request.session['bid'] = cn.id

        for x in range(1, cn.book_copies+1):
            count.append(x)

        context['count'] = count
        context['cobj'] = cobj = Categories.objects.all()
        context['bobj'] = bobj = Books.objects.all()
        context['bcobj'] = bcobj = Book_comments.objects.all()

        if request.method == 'POST':
            if request.session.has_key('user_mail'):
                ctext = request.POST.get('ctext')
                if ctext != '':
                    obj = Book_comments.objects.create(book_title=cn.book_title, book_comment=ctext, book_user_mail=user_mail)
                    obj.save()
    else:
        return redirect('login')

    return HttpResponse(template.render(context, request))

def logout(request):
    template = loader.get_template('logout.html')
    context = {'mess': ''}

    request.session.flush()

    return redirect('index')

def forgot(request):
    template = loader.get_template('forgot.html')
    context = {'mess': "", 'tfmess': 'False'}
    uobj = Users.objects.all()

    if request.method == 'POST':

        user_password = request.POST.get('user_password')
        user_mail = request.POST.get('user_mail')
        user_name = request.POST.get('user_name')
        c = 0
        for x in uobj:
            if x.user_mail == user_mail and x.user_name == user_name:
                context['mess'] = ''
                uuobj = x
                c = 1

        if context['mess'] != '':
            context['mess'] = 'Please Enter Details correctly'

        if context['mess'] == '' and c == 1:
            uuobj.user_password = user_password
            uuobj.save()

            context['mess'] = 'Password Changed'

    return HttpResponse(template.render(context, request))
#--------------------- provider -------------------

def pro_category(request):
    template = loader.get_template('provider/pro_category.html')
    context = {'tfmess': 'False'}
    context['cateobj'] = cateobj = Categories.objects.order_by('category_name')
    context['bobj'] = bobj = Books.objects.all()
    context['robj'] = robj = Rating.objects.all()

    return HttpResponse(template.render(context,request))

def pro_category_items(request,prod_id):
    template = loader.get_template('provider/pro_category_items.html')
    context = {'mess': "", 'tfmess': 'False'}
    val = 0

    if request.session.has_key('user_mail'):
        context['user_mail'] = user_mail = request.session['user_mail']
        context['tfmess'] = 'True'

    context['cn'] = cn = Categories.objects.get(id=prod_id)

    context['cobj'] = cobj = Categories.objects.order_by('category_name')
    context['bobj'] = bobj = Books.objects.all()

    for x in bobj:
        if x.book_category == cn.category_name:
            val = 1

    if val == 0:
        context['mess'] = 'No books Available'

    return HttpResponse(template.render(context, request))

def pro_home(request):
    template = loader.get_template('provider/pro_home.html')
    context = {'mess': ""}

    uobjmail = request.session['user_mail']
    context['bobj'] = bobj = Books.objects.all()

    return HttpResponse(template.render(context, request))

def pro_add_book(request):
    template = loader.get_template('provider/pro_add_book.html')
    context = {'mess': ""}
    context['cateobj'] = cateobj = Categories.objects.order_by('category_name')
    bobj = Books.objects.all()
    uobjmail = request.session['user_mail']

    if request.method == 'POST':
        context['val'] = 'no'
        title = (request.POST.get('book_title')).title()
        genre =(request.POST.get('bgenre'))
        isbn =(request.POST.get('bisbn'))
        author =(request.POST.get('bauthor')).title()
        publisher =(request.POST.get('bpub')).title()
        copies =(request.POST.get('bcopies'))
        price =(request.POST.get('bprice'))
        lang =(request.POST.get('blang')).title()
        year =(request.POST.get('byear'))
        desc =(request.POST.get('bdes'))
        fupload = request.FILES['bphoto']

        if len(isbn) != 10:
            context['mess'] = 'enter proper ISBN10'

        if len(year) != 4:
            context['mess'] = 'enter proper year'

        for x in bobj:
            if x.book_title == title:
                context['mess'] = 'Title Already Exist'

        try:
            isbn = int(isbn)
        except:
            context['mess'] = 'enter proper ISBN10'

        try:
            year = int(year)
        except:
            context['mess'] = 'enter proper year'

        if context['mess'] == '':
            upobj = Books.objects.create(
                book_title=title,
                book_author=author,
                book_copies=copies,
                book_description=desc,
                book_image=fupload,
                book_isbn10=isbn,
                book_provider_mail=uobjmail,
                book_year=year,
                book_publisher=publisher,
                book_price=price,
                book_language=lang,
                book_category=genre
            )

            upobj.save()
            context['mess'] = 'Book added Successfully'

    return HttpResponse(template.render(context, request))

def pro_del_book(request):
    template = loader.get_template('provider/pro_del_book.html')
    context = {'mess': ""}

    uobjmail = request.session['user_mail']
    context['bobj'] = bobj = Books.objects.all()

    if request.method == 'POST':
        delbook = int(request.POST.get('delbook'))
        delobj = Books.objects.get(id=delbook)
        delobj.delete()
        context['mess'] = 'Book Deleted'
    return HttpResponse(template.render(context, request))

def pro_report(request):
    template = loader.get_template('provider/pro_reports.html')
    context = {'mess': ""}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    return HttpResponse(template.render(context, request))

def pro_add_cate(request):
    template = loader.get_template('provider/pro_add_cate.html')
    context = {'mess': ""}
    context['cobj'] = cobj = Categories.objects.order_by('category_name')

    if request.method == 'POST':
        cate = str(request.POST.get('cate')).title()
        fimg = request.FILES['fimg']

        for x in cobj:
            if x.category_name.title() == cate:
                context['mess'] = 'Categories already exists'

        if context['mess'] == '':

            obj = Categories.objects.create(
                category_name=cate,
                category_image=fimg
            )

            obj.save()

            return redirect('pro_add_cate')

    return HttpResponse(template.render(context, request))

def pro_del_cate(request):
    template = loader.get_template('provider/pro_del_cate.html')
    context = {'mess': ""}
    context['cobj'] = cobj = Categories.objects.order_by('category_name')

    if request.method == 'POST':
        cate_id = int(request.POST.get('cate_id'))
        delobj = Categories.objects.get(id=cate_id)

        for x in Books.objects.all():
            if x.book_category == delobj.category_name:
                x.delete()

        delobj.delete()
        context['mess'] = 'Category Deleted'

    return HttpResponse(template.render(context, request))

#--------------------- customer -------------------

def cart0(request):
    template = loader.get_template('cart0.html')
    context = {'mess': "single", 'tot': '', 'tfmess': 'False'}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    tit,c,id = '',0,0
    if request.session.has_key('user_mail'):
        context['user_mail'] = user_mail = request.session['user_mail']
        context['tfmess'] = 'True'

        if request.session.has_key('bid'):
            context['bid'] = bid = request.session['bid']
            selno = request.POST.get('selno')
            selno = int(selno)

            bdelobj = Books.objects.get(id=bid)

            for n in cobj:
                if n.mail == user_mail and bdelobj.book_title == n.book_title and n.status == 'no':
                    c = 1
                    n.cost += int(int(bdelobj.book_price) * int(selno))
                    n.items += selno
                    n.save()

            if c == 0:
                cmobj = Cart.objects.create(
                    book_id= bid,
                    book_title= bdelobj.book_title,
                    mail= user_mail,
                    cost=(int(bdelobj.book_price) * int(selno)),
                    items=selno
                )
                cmobj.save()
            bdelobj.book_copies -= int(selno)
            bdelobj.save()

            return redirect('cart')
    else:
        return redirect('login')

def cart(request):
    template = loader.get_template('cart.html')
    context = {'mess': "", 'tot':0, 'dis': ''}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    if request.session.has_key('user_mail'):
        context['user_mail'] = user_mail = request.session['user_mail']
        context['tfmess'] = 'True'
        context['addr'] = addr = Users.objects.get(user_mail=user_mail)

        for x in Cart.objects.all():
            if x.status == 'no1' and x.mail == user_mail:
                x.status = 'no'
                x.save()

        for b in bobj:
            for c in cobj:
                if c.mail == user_mail and c.book_title == b.book_title and c.status == 'no':
                    context['dis'] = 'yes'

        if request.method == 'POST':
            citems = request.POST.getlist('citems')
            sel = request.POST.get('sel')
            if citems:
                if sel == 'cartproceed':
                    for citem in citems:
                        item = int(citem)
                        obj = Cart.objects.get(id=item)
                        obj.status = 'no1'
                        obj.save()
                    return redirect('cartconfirm')

                if sel == 'cartdel':
                    for citem in citems:
                        item = int(citem)
                        obj = Cart.objects.get(id=item)
                        delobj = Books.objects.get(book_title=obj.book_title)
                        delobj.book_copies += int(obj.items)
                        delobj.save()
                        obj.delete()
                        return redirect('cart')

            else:
                context['mess'] = 'Please select minimum one option'

    return HttpResponse(template.render(context, request))

def cartconfirm(request):
    template = loader.get_template('cartconfirm.html')
    context = {'mess': "", 'tot':0, 'tfmess': 'False'}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    cost = 0
    context['user_mail'] = user_mail = request.session['user_mail']
    context['tfmess'] = 'True'
    context['addr'] = addr = Users.objects.get(user_mail=user_mail)
    context['cardobj'] = cardobj = Card_details.objects.get(card_mail=user_mail)

    for x in Cart.objects.all():
        p = 0
        if x.status == 'no1' and x.mail == user_mail:
            p = int(x.cost)
            cost += p
    context['tot'] = cost

    if request.method == 'POST':
        uobj = Users.objects.get(user_mail=user_mail)
        caddr1 = request.POST.get('caddr1')
        caddr2 = request.POST.get('caddr2')
        rating_value = request.POST.get('eradio')
        bval = request.POST.get('bradio')
        cardname = request.POST.get('cardname')
        card = request.POST.get('card')
        cvv = request.POST.get('cvv')
        sdet = request.POST.getlist('savedet')

        if rating_value == 'nval':
            if len(caddr2) > 0:
                context['mess'] = ''
            else:
                context['mess'] = 'Enter Proper Address'

        if bval == 'eval':
            if len(card) == 12 and len(cvv) == 3 and len(cardname) > 0:
                try:
                    cd = int(card)
                    cv = int(cvv)
                    if sdet:
                        cdobj = Card_details.objects.get(card_mail=user_mail)
                        cdobj.card_name = cardname
                        cdobj.card_number = card
                        cdobj.card_cvv = cvv
                        cdobj.save()
                except:
                    context['mess'] = 'enter card details properly'
            else:
                context['mess'] = 'enter card details properly'

        if context['mess'] == '':

            for c in bobj:
                for b in cobj:
                    if b.book_title == c.book_title and b.status == 'no1':
                        b.status = 'yes'
                        b.save()
                        uorder = Orders.objects.create(
                            order_mail=user_mail,
                            order_title=c.book_title,
                            order_author=c.book_author,
                            order_copies=b.items,
                            order_description=c.book_description,
                            order_image=c.book_image,
                            order_isbn10=c.book_isbn10,
                            order_provider_mail=c.book_provider_mail,
                            order_year=c.book_year,
                            order_publisher=c.book_publisher,
                            order_price=b.cost,
                            order_language=c.book_language,
                            order_category=c.book_category,
                            order_rating=c.book_rating
                        )
                        uorder.save()

            context['tot'] = 0

            if rating_value == 'eval':
                uobj.save()
                context['mess'] = 'Orders placed successfully'

            if rating_value == 'nval':
                if caddr2 != '' or caddr2 != None:
                    uobj.user_address = caddr2
                    uobj.save()
                    context['mess'] = 'Orders placed successfully'





    return HttpResponse(template.render(context, request))

def orders(request):
    template = loader.get_template('orders.html')
    context = {'mess': "", 'tfmess': 'False','dis':''}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()
    context['robj'] = robj = Rating.objects.all()
    context['oobj'] = oobj = Orders.objects.all()
    con = 0
    for o in oobj:
        con = 0
        for b in bobj:
            if o.order_title == b.book_title:
                con = 1

        if con == 0:
            o.order_status = 'off'
            o.save()

    c,t,ctot = 0,0,0
    for b in bobj:
        c,t,ctot = 0,0,0
        for r in robj:
            if b.book_title == r.title:
                ctot += 1
                context['dis'] = 'y'
        for r in robj:
            if b.book_title == r.title:
                 c += int(r.rating_value)

        if ctot > 0:
            t = float(c/ctot)
            t = round(t, 1)

        b.book_rating = float(t)
        b.save()

    for b in bobj:
        for o in oobj:
            if b.book_title == o.order_title:
                o.order_rating = b.book_rating
                o.save()

    if request.session.has_key('user_mail'):
        context['user_mail'] = user_mail = request.session['user_mail']
        context['tfmess'] = 'True'

        for x in cobj:

            if x.mail == user_mail and x.status == 'yes':
                c = 1
                context['mess'] = ''
                context['dis'] = 'y'
        if c == 0:
            context['mess'] = 'No orders to display'
            context['dis'] = ''

        if context['mess'] == '':
            if request.method == 'POST':
                selid = int(request.POST.get('selid'))
                selrating = int(request.POST.get('selrating'))
                orderobj = Orders.objects.get(id=selid)

                for x in Books.objects.all():
                    if x.book_title == orderobj.order_title:
                        obj = Rating.objects.create(
                            user_mail=user_mail,
                            title=x.book_title,
                            rating_value=selrating
                        )
                        obj.save()

                        for o in oobj:
                            if x.book_title == o.order_title:
                                o.order_rating = x.book_rating
                                o.save()

                return redirect('orders')

    return HttpResponse(template.render(context, request))

def account(request):
    template = loader.get_template('account.html')
    context = {'mess': "", 'tfmess': 'False'}
    context['user_mail'] = user_mail = request.session['user_mail']
    context['tfmess'] = 'True'
    context['uobj'] = uobj = Users.objects.get(user_mail=user_mail)

    if request.method == 'POST':

        uuobj = Users.objects.get(id=uobj.id)
        user_password = request.POST.get('user_password')
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        user_address = request.POST.get('user_address')
        user_number = request.POST.get('user_number')


        try:
            if len(user_number) != 10:
                context['mess'] = 'Enter Proper Phone Number'
            user_number = int(user_number)
        except:
            context['mess'] = 'Enter Proper Phone Number'

        if context['mess'] == '':
            uuobj.user_password = user_password
            uuobj.first_name = first_name
            uuobj.second_name = second_name
            uuobj.user_address = user_address
            uuobj.user_number = user_number
            uuobj.save()
            context['mess'] = 'Account Details Updated'

    return HttpResponse(template.render(context, request))

