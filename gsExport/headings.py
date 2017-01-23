from datetime import datetime
from pytz import timezone
import pytz
import nbformat.notebooknode as nn


_header_node = {'cell_type': 'markdown',
  'execution_count': None,
  'source': '',
  'metadata':{}}


def generate_header():
	date_format='%m/%d/%Y %H:%M:%S %Z'
	date = datetime.now(tz=pytz.utc)
	date = date.astimezone(timezone('US/Pacific'))
	results_node = _header_node.copy()
	results_node['source'] = 'Local date & time is  :', date.strftime(date_format)
	return nn.NotebookNode(results_node)
