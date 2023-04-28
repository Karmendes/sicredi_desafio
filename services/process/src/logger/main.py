from datetime import datetime
from termcolor import colored, cprint


def get_debug_text(message):
  out_message=f'# {message}'
  if len(out_message) <= 88:
    length_diff = 88 - len(out_message)
    separators='='*length_diff
    out_message=f'{out_message} {separators}#'

  return out_message


class Logger:
  
  ERROR = 'ERROR'
  INFO = 'INFO'
  WARNING = 'WARNING'
  DEBUG = 'DEBUG'

  @staticmethod
  def emit(message='', log_type='INFO'):
    out_message=message
    if Logger.DEBUG == log_type:
      out_message=get_debug_text(out_message)
    text = colored(f"[{datetime.now()}]  [{log_type}] - {out_message}")
    cprint(text, Logger._get_color(log_type))

  @staticmethod
  def _get_color(log_type):
    if Logger.ERROR == log_type:
        return 'red'
    elif Logger.WARNING == log_type:
        return 'yellow'
    else:
        return 'white'