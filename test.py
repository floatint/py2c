class Def:
   print("sds")
   def a(self):
      print(100)

#Def().a()

def gen():
   for i in range(10):
      yield i

def a(a,b,c = 10):
   print(f"{a}{b}")
   print([str(i) for i in range(10)])

def func(a, b, *args, key=True, **kwargs):
   # "OO|O&OO"
   c = a + b  # c - local

   def func2(r):
      return r + c
   return func2
