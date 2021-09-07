from typing import List


template1 = """
from fastapi import FastAPI
from {path} import {class_name}
import uvicorn
app = FastAPI()
file = r"{file_path}"
{func_name}={class_name}()
@app.get("/")
def hello_world():
    msg="Welcome to my FastAPI project!"\
        "Please visit the /docs to see the API documentation."
    return msg\n
    """
template2 = """
# WARNING:DO NOT EDIT THE BELOW LINE
app.add_api_route(
        path="/{route_path}",
        endpoint={endpoint},
        methods={http_methods},
    )\n
        """
template3 = """
if __name__ == "__main__":
    try:
        {func_name}.artifacts.load_all(file)
    except:
        print("failed to load model or didn't find any.")
    uvicorn.run(
            app=app,
            host='0.0.0.0',
            port=5000
        )\n"""

class InferenceAPI(object):
    """
    InferenceAPI defines an inference call to the underlying model, including its input
    and output adapter, the user-defined API callback function, and configurations for
    working with the BentoML adaptive micro-batching mechanism
    """

    def __init__(
        self,
        service,
        name,
        doc,
        user_func: callable,
        mb_max_latency=10000,
        mb_max_batch_size=1000,
        batch=False,
        route=None,
        http_methods=None,
    ):
      self._service = service
      self._name = name
      self._user_func = user_func
      self.mb_max_latency = mb_max_latency
      self.mb_max_batch_size = mb_max_batch_size
      self.batch = batch
      self._http_methods = http_methods
      self.route = name if route is None else route

def api_decorator(
    *args,
    api_name: str = None,
    route: str = None,
    api_doc: str = None,
    http_methods: List[str] = None,
    **kwargs,
):  # pylint: disable=redefined-builtin

    def decorator(func):
        _api_name = func.__name__ if api_name is None else api_name
        _api_route = _api_name if route is None else route
        _api_doc = func.__doc__ if api_doc is None else api_doc
        _http_methods = http_methods if http_methods else ['GET']
        setattr(func, "_is_api", True)
        setattr(func, "_api_name", _api_name)
        setattr(func, "_api_route", _api_route)
        setattr(func, "_api_doc", _api_doc)
        setattr(func, "_http_methods", _http_methods)
        return func

    return decorator

class LambdaService:
    # List of inference APIs that this BentoService provides
    _inference_apis: List[InferenceAPI] = []

    # Name of this BentoService. It is default the class name of this BentoService class
    _lambda_service_name: str = None

    #  A `BentoServiceEnv` instance specifying the required dependencies and all system
    #  environment setups
    _env = None

    # When loading BentoService from saved bundle, this will be set to the version of
    # the saved BentoService bundle
    _bento_service_bundle_version = None

    # See `ver_decorator` function above for more information
    _version_major = None
    _version_minor = None

    # See `web_static_content` function above for more
    _web_static_content = None

    def __init__(self):
        # When creating BentoService instance from a saved bundle, set version to the
        # version specified in the saved bundle
        self._bento_service_version = self.__class__._bento_service_bundle_version
        self._config_artifacts()
        self._config_inference_apis()
        self._config_environments()

    def create_fastapi_file(class_name, module_name, apis_list, store_path):
        import os
        path = f"{class_name}.{module_name}"
        file_path = os.path.join(f"{class_name}","artifacts")
        store_path = os.path.abspath(os.curdir) + '\\build\\api.py'

        func_name = class_name.lower() + "_func"
        complete_template = template1.format(
            path=path,
            class_name=class_name,
            file_path=file_path,
            func_name=func_name
        )

        for api in apis_list:
            complete_template += template2.format(
                route_path=api.route,
                endpoint=f"{func_name}.{api.name}",
                http_methods=api.http_methods
            )

        complete_template += template3.format(
            func_name=func_name
        )

        try:
            with open(store_path, "x") as f:
                f.write(complete_template)
        except FileExistsError:
            raise Exception("The FastAPI file already exists")
