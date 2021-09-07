
from click import ClickException
import click
import sys
def _echo(message, color="reset"):
    click.secho(message, fg=color)

def save_direct(
            path
    ):
        if path[-2:] != "py":
            raise Exception("the file is not a python file")

        import os
        import importlib
        import inspect
        from bentoml import BentoService
        complete_path = os.path.join(os.getcwd(), path)
        head, module_name = os.path.split(complete_path)
        sys.path.append(head)
        module_name = module_name[:-3]
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            raise Exception(f"Couldn't import module:", e)

        count = 0
        class_names = []
        for name, obj in inspect.getmembers(module):
            try:
                if inspect.isclass(obj) and issubclass(obj, BentoService) and \
                        getattr(obj, '__module__', None).split(".")[0] != "bentoml":
                    count += 1
                    class_names.append(obj.__name__)
            except:
                pass
        _echo(f"Found {count} classes to save")
        for i in class_names:
            try:
                init = getattr(module, i)
                init().save()
            except Exception as e:
                _echo(f"Couldn't save {i}")
        _echo("Saved all the necessary modules.")
