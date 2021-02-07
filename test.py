def ar(a,b,c = 10):
   a = 100
   def g():
      print(a)

def func(a, b, *args, key=True, **kwargs):
   # "OO|O&OO"
   c = a + b  # c - local

   def func2(r):
      return r + c
   return func2
