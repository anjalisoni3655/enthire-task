

from bentoml import env, artifacts, api, BentoService

# BentoML packages local python modules automatically for deployment
from my_ml_utils import my_encoder

@env(infer_pip_packages=True)
class MyService(MyLibrary.LambdaService):
   """
   User will write a class which will extend a predefined class (from the library you make) called LambdaService.
   """
   @api(method=Mylibrary.methods.GET)
   #@api(http_methods=['GET'],api_name="predict")
   def predict(self, a: int, b: int):
       """
         Users will write methods in this class and annotate them with the decorator @api. Only some methods will be annotated
       as @api and some might not be.
       """
       sum = a + b
       return sum
