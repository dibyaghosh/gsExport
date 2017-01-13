from IPython import get_ipython
from client.api.assignment import load_assignment
import glob
import nbformat.notebooknode as nn
import os, contextlib

__runner = """
from client.api.assignment import load_assignment
import glob


ga_autograder = load_assignment("{ok_file}")
ga_tests = sorted([s.rsplit('/')[-1].split('.')[0] for s in glob.glob("tests/q*")])
ga_test_results = []

for _test in ga_tests:
    res_question = ga_autograder.grade(_test)
    q_all = sum(res_question.values())
    q_right = res_question['passed']
    test_dict = [_test,q_right, q_all,round(q_right/q_all*100)]
    ga_test_results.append(test_dict)
"""

_ok_results_node = {'cell_type': 'markdown',
  'execution_count': None,
  'source': '',
  'metadata':{}}


def __autograde():
	possible_ok_files = glob.glob("*.ok")
	if len(possible_ok_files) == 0:
		print("Couldn't find the ok file")
		return
	ok_file = possible_ok_files[0]
	print("Grading using the %s file"%ok_file)
	python_instance = get_ipython()
	with open(os.devnull, 'w') as devnull:
		with contextlib.redirect_stdout(devnull):
			python_instance.ex(__runner.format(ok_file=ok_file))
	test_results = python_instance.ev("ga_test_results")
	return "Test Name | Score | Possible | Percent Tests Passed\n --- | --- | --- | --- \n"+"\n".join(["|".join(list(map(str,test))) for test in test_results])


def autograde_ipython():
	"""
		Returns a notebook node
	"""
	results_node = _ok_results_node.copy()
	results_node['source'] = __autograde()
	return nn.NotebookNode(results_node)
