import numpy as np
import MyLibrary.service as MyLibrary
import MyLibrary.service.api_decorator as api

class MyService(MyLibrary.LambdaService):
   """
   User will write a class which will extend a predefined class (from the library you make) called LambdaService.
   """
   @api(http_methods=["GET"])
   def sum(self, a: int, b: int):
       """
         Users will write methods in this class and annotate them with the decorator @api. Only some methods will be annotated
       as @api and some might not be.
       """
       a = 4
       b = 6
       sum = a + b
       return sum

   @api(http_methods=["GET"])
   def npArr(self, a: int, b: int):
      arr = np.array( [[ 1, 2, 3],
                 [ 4, 2, 5]] )
      return arr.shape


