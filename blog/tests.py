from django.test import TestCase

# Create your tests here.

from django.test import Client
from lxml import html, etree

class verifyLinks(TestCase):

    def setUp(self):
        pass
        c = Client()
        response = c.get('/site_map')
        #print(response.content)        

        #c.get('/customers/details/', {'name': 'fred', 'age': 7})
        #response = c.post('/login/', {'username': 'john', 'password': 'smith'})
        #response.status_code

        self.n = 0
        self.problems = []
        
        #create HtmlElement instance
        doc = html.fromstring(response.content)
        anchors = doc.xpath('//a')
        for anchor in anchors:
            try:
                link = anchor.get('href')
                #print(link)
                response = c.get(link)   
                if(response.status_code != 200):
                    self.n += 1
                    self.problems.append('{} err:{}'.format(link,response.status_code))
            except Exception as e:
                self.n += 1
                #print('Error: {c}, Message: {m}'.format(c = type(e).__name__, m = str(e)))
                self.problems.append('{} err:{} {}'.format(link,type(e).__name__,str(e)))

        #print(problems)
        

    def test_links(self):

        if(self.n != 0):
            print("\nFailed links:")
            for p in self.problems:
                print(p)

        self.assertIs(self.n, 0)
        #self.assertEqual(result(), 'test')



