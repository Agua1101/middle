from dangdangapp.models import TBook


class CartItem():
    def __init__(self,book,amount):
        self.amount = amount
        self.book = book
        self.status = 1

class Cart():
    def __init__(self):
        self.save_price = 0
        self.total_price = 0
        self.cartItem = []


    def sums(self):
        self.total_price = 0
        self.save_price = 0
        for i in self.cartItem:
            self.total_price += i.book.dang_price * i.amount
            self.save_price += (i.book.market_price - i.book.dang_price) * i.amount

    def add_book_toCart(self,bookid,amount):
        for i in self.cartItem:
            if i.book.id == int(bookid):
                i.amount += int(amount)
                self.sums()
                return
        book = TBook.objects.filter(id = bookid)[0]
        self.cartItem.append(CartItem(book,amount))
        self.sums()

    def change_book(self,bookid,amount):
        for i in self.cartItem:
            if i.book.id == int(bookid):
                i.amount = int(amount)
                self.sums()
                return
        book = TBook.objects.filter(id = bookid)[0]
        self.cartItem.append(CartItem(book,amount))
        self.sums()

    def modify_cart(self,bookid,amount):
        for i in self.cartItem:
            if i.book.id == int(bookid):
                i.amount = int(amount)
        self.sums()

    def delete_book(self,bookid):
        for i in self.cartItem:
            if i.book.id == int(bookid):
                self.cartItem.remove(i)
        self.sums()

    # def recover_book(self, bookid):
    #     for i in self.cartItem:
    #         if i.book.id == int(bookid):
    #             self.cartItem.append(i)


class ReCart():
    def __init__(self):
        self.save_price = 0
        self.total_price = 0
        self.cartItem_del = []

    def recover_book(self,bookid):
        for i in self.cartItem_del:
            if i.book.id == int(bookid):
                self.cartItem_del.remove(i)

    def delete_book(self,bookid,amount):
        for i in self.cartItem_del:
            if i.book.id == int(bookid):
                i.amount += int(amount)
                return
        book = TBook.objects.filter(id=bookid)[0]
        self.cartItem_del.append(CartItem(book, amount))
