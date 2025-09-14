# あおい作業用

from database import *

shironingen = Person(name='しろにんげん', age=32)
okazu = Person(name='おかず担当大臣', age=20)
hohoemi = Person(name="ほほえみさん",age = 36)

shironingen.save()
okazu.save()
hohoemi.save()