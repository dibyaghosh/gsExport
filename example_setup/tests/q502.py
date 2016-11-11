test = {
  'name': 'Question',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> type(hello_world_components)
          numpy.ndarray
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> len(hello_world_components)
          5
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> import numpy as np
          >>> all(hello_world_components == np.array(["Hello", ",", " ", "world", "!"]))
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
