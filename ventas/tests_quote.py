import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Quote
from personal.models import Client
from personal.models import Executive
from personal.models import Person
from recursos.models import Paper


class QuoteSetUpClass(TestCase):
    def setUp(self):
        person = Person.objects.create(
            person_name='Andy',
            person_lastname='Sapper')
        self.client_instance = Client.objects.create(
            client_name='Test_Client',
            client_receipt_name='Test_Client',
            client_receipt_address='123 ave',
            client_nit=123456)
        self.executive_instance = Executive.objects.create(
            person=person,
            executive_comssn=10)
        self.paper_instance = Paper.objects.create(
            paper_name='Test_Paper',
            paper_width=10,
            paper_length=10,
            paper_price=0.5)

    def create_quote(self, name, due_date, copies, product_name, width, length,
                     bleed, sides, colors_front, colors_back):
        """Create a Quote with the given information."""
        return Quote.objects.create(
            quote_name=name,
            quote_due_date=due_date,
            quote_copies=copies,
            quote_product_name=product_name,
            quote_dimention_width=width,
            quote_dimention_length=length,
            quote_printing_bleed=bleed,
            quote_printing_sides=sides,
            quote_printing_colors_front=colors_front,
            quote_printing_colors_back=colors_back,
            client=self.client_instance,
            executive=self.executive_instance,
            paper=self.paper_instance)


class QuoteViewTests(QuoteSetUpClass, TestCase):
    def test_quote_view_with_no_quotes(self):
        """If no Quotes exist, an appropriate message should be displayed."""
        response = self.client.get(reverse('ventas:quotes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No quotes are available.")
        self.assertQuerysetEqual(response.context['latest_quote_list'], [])

    def test_quote_view_with_a_quote(self):
        """If a Quote exists, it should be displayed."""
        self.create_quote(name="Quote1", due_date=datetime.date.today(),
                          copies=10, product_name="Prueba", width=10,
                          length=18, bleed=0.1, sides=2, colors_front=4,
                          colors_back=4)
        response = self.client.get(reverse('ventas:quotes'))
        self.assertQuerysetEqual(
            response.context['latest_quote_list'],
            [("<Quote: Id: 1; Name: Quote1; Product: Prueba; "
                "Dimentions: 10.00\" x 18.00\"; Due: {}; Copies: 10; "
                "Printing sides: 2.>").format(datetime.date.today())]
        )

    def test_quote_view_with_two_quotes(self):
        """If two or more Quotes exist, they should be displayed."""
        # create quote #1
        self.create_quote(name="Quote1", due_date=datetime.date.today(),
                          copies=10, product_name="Prueba", width=10,
                          length=18, bleed=0.1, sides=2, colors_front=4,
                          colors_back=4)
        # create quote #2
        self.create_quote(name="Quote2", due_date=datetime.date.today(),
                          copies=20, product_name="Prueba2", width=11,
                          length=19, bleed=0.1, sides=1, colors_front=0,
                          colors_back=4)
        # get response
        response = self.client.get(reverse('ventas:quotes'))
        self.assertQuerysetEqual(
            response.context['latest_quote_list'].order_by('id'),
            [("<Quote: Id: 1; Name: Quote1; Product: Prueba; "
                "Dimentions: 10.00\" x 18.00\"; Due: {}; Copies: 10; "
                "Printing sides: 2.>").format(
                    datetime.date.today()),
             ("<Quote: Id: 2; Name: Quote2; Product: Prueba2; "
                "Dimentions: 11.00\" x 19.00\"; Due: {}; Copies: 20; "
                "Printing sides: 1.>").format(
                    datetime.date.today())]
        )


class QuoteMethodTests(QuoteSetUpClass, TestCase):
    def test_get_quote_id(self):
        """Create a quote, and get its id."""
        # create quote with id: 1
        quote = self.create_quote(name="Quote1",
                                  due_date=datetime.date.today(), copies=10,
                                  product_name="Prueba", width=10, length=18,
                                  bleed=0.1, sides=2, colors_front=4,
                                  colors_back=4)
        # check method: get_quote_id()
        self.assertEqual(quote.get_quote_id(), 1)

    def test_get_due_date(self):
        """Create a quote, and get its id."""
        today = datetime.date.today()
        # create quote with due date: today
        quote_today = self.create_quote(name="Quote1", due_date=today,
                                        copies=10, product_name="Prueba",
                                        width=10, length=18, bleed=0.1,
                                        sides=2, colors_front=4, colors_back=4)
        # create quote with due date: today
        in_seven_days = today + datetime.timedelta(days=7)
        quote_future = self.create_quote(name="Quote2", due_date=in_seven_days,
                                         copies=20, product_name="Prueba2",
                                         width=10, length=18, bleed=0.1,
                                         sides=1, colors_front=4,
                                         colors_back=4)

        # check method: get_quote_due_date()
        self.assertEqual(quote_today.get_due_date(), today)
        self.assertEqual(quote_future.get_due_date(), in_seven_days)
