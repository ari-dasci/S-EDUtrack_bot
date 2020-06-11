import logging
import inspect
import sys
from colorama import init, Fore, Back
import general_funtions as g_fun

# Configurar logging
logging.basicConfig(
  level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()


def print_except(function, *extra_info):
  try:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    function += f" line:{exc_tb.tb_lineno}"
    error_text = f"""
    ====================
    ERROR IN FUNCTION {function}
    {exc_type}
    {exc_obj}
    """
    if extra_info:
      for element in extra_info:
        error_text += "\n" + element
    error_text += "===================="
    print(Back.RED)
    logger.info(error_text + Back.RESET)
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
