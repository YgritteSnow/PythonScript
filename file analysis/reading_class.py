
class ClassNode(object):

	def __init__(self, name, fatherlist, childrenlist, funclist, others=None):
		super(ClassNode, self).__init__()
		self._name = name
		self._fatherlist = fatherlist
		self._childrenlist = childrenlist
		self._funclist = funclist
		self._others = others

def ClassNodeGenerate(*arg, **kwargs):
	ClassNode(*arg, **kwargs)


class WordNode(object):

	def __init__(self, name, frequency, desc, linkedwords = ()):
		super(WordNode, self).__init__()
		self._name = name
		self._frequency = frequency
		self._desc = desc
		self._linkedwords = linkedwords

def WordNodeGenerate(*arg, **kwargs):
	WordNode(*arg, **kwargs)