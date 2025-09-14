# かずのり作業用

from database import *

rituki = Person(name='高宮律樹', age=12)
keito = Person(name='齋藤慶人', age=13)
kouto = Person(name='熊谷洸人', age=13)

rituki.save()
keito.save()
kouto.save()