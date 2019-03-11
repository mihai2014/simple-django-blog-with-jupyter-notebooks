Files are stored in 'blog/templates/blog/data/'

There are two formats:

	1)Html file(data codes are google prettyfied):
	(see example1.html)

	2)Notebook(jupyter) in format html(example2.htm.example2.html)
	Each notebook.html must be "doubled" by a notebook.htm template
	Notebooks are loaded using an iframe. 

Javascript notebook dependence could be loaded from local (blog/static/blog/js/MathJax must be created) by setting LOCAL_NOTEBOOK = True in views.py


