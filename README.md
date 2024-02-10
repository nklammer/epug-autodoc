# Building the Web Documentation

This is a guide for how to build the API documentation for the `epug` package used by Affiliated Engineers. The upfront effort in setting up the software build is more than justified by the benefit of automatic generation of documentation using the embedded Python docstrings.

## Build Environment

### Python 3.8.X

### epug Anaconda Environment
Circa June 2023. Can be overriden with a `requirement.txt` file in the repository.

Run this build from Anaconda command with the `epug` Anaconda environment active.

```(base) $ C:\Users\puggy\Documents\GitHub>activate epug``` 

results in 
```(epug) $ C:\Users\puggy\Documents\GitHub\epug>```


### Sphinx 5.2.3
```$ pip install sphinx```

### sphinx_rtd_theme 1.0.0
```$ pip install sphinx_rtd_theme```


## Steps

### Make directory and navigate to

```
$ C:\Users\puggy\Documents\GitHub\epug\documentation>mkdir sphinx_root
$ C:\Users\puggy\Documents\GitHub\epug\documentation>
```
"sphinx_root" will be your Sphinx Root Directory.

### Run `sphinx-quickstart`

```
$ C:\Users\puggy\Documents\GitHub\epug\documentation\web_docs>sphinx-quickstart sphinx_root
```

Enter through all the arguments (Project Name, Author, "Y" to separate source and build directories). The Sphinx Root Directory now looks like this:

```
sphinx_root
  |
  |__build
  |__source
  |    |__conf.py
  |    |__index.rst
  |    |__...
  |__make.bat
  |__Makefile
```
### Check Step: Build the skeleton index.rst
```
$ sphinx-build -M html sphinx_root/source/ sphinx_root/build/
```


### Edit the `source\conf.py` file

See the code block at the bottom of this guide.

* `import os, sys`
* `sys.path.insert(0, os.path.abspath('../../../src'))`
* `sys.path.insert(0, os.path.abspath('.'))`
* `print(str(sys.path))` # so you can check that you correctly added the source files to the path
* `extensions = ['sphinx.ext.autodoc', 'numpydoc', 'sphinx.ext.autosummary', 'sphinx.ext.napoleon']`
* `autodoc_default_options = {'members': True, 'undoc-members': True, 'special-members': False, 'inherited-members': True, 'show-inheritance': True }`
* `napoleon_google_docstring = False`
* `napoleon_numpy_docstring = True`
* `html_theme = 'sphinx_rtd_theme`
     `

### sphinx-apidoc [(link)](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html#sphinx-apidoc)

sphinx-apidoc is a tool for automatic generation of Sphinx sources that, using the autodoc extension, documents a whole package in the style of other automatic API documentation tools. sphinx-apidoc generates source files that use `sphinx.ext.autodoc` to document all found modules.  Use `--separate` option for more pages. Use the `--force` option for overriding the stubs. Use the `--implicit-namespaces` option to look for namespace packages (vs. regular packages, the primary distinction is the inclusion of the `__init__.py`). Note that the MODULE_PATH arg is relative to the Sphinx wdir in `/docs/` 

```
sphinx-apidoc -o <OUTPUT> <SOURCE_FILES>
```

So for example that looks like this:

```
$ C:\Users\puggy\Documents\GitHub\epug\documentation\web_docs>sphinx-apidoc --force --implicit-namespaces --separate -o ./source ../../src/bpp
```

Output:
```
(epug) C:\Users\nklammer\Documents\GitHub\epug\documentation\web_docs>sphinx-apidoc -o ./source ../../src/bpp
Creating file ./source\bpp.rst.
Creating file ./source\bpp.air_systems.rst. 
Creating file ./source\bpp.architecture.rst.
Creating file ./source\bpp.modeling.rst.
Creating file ./source\bpp.plant.rst.
Creating file ./source\bpp.program.rst.
Creating file ./source\bpp.project.rst.
Creating file ./source\bpp.reporting.rst.
Creating file ./source\bpp.reporting.QC.rst.
Creating file ./source\bpp.schedules.rst.
Creating file ./source\bpp.ui_functions.rst.
Creating file ./source\bpp.weather.rst.
Creating file ./source\modules.rst.
```

#### `sphinx-apidoc`
This CLI command generates "stubs" for each of your modules. The stubs contain `automodule::` ReST directives which in turn inform `sphinx-build` (aliased through `make html`) to invoke `autodoc` to do the heavy lifting of actually generating the API documentation from the docstrings of a particular module. I've found that out of the box, I just get a screenful of `ImportError`'s from `autodoc` during `sphinx-build`.

To ensure that `sphinx-build` can import your package and generate some lovely API documentation (and that all important module index; `py-modindex`), simply uncommment this line near the top of the `conf.py` and those warnings should disappear.

### sphinx.ext.autodoc
Continuing, if we want Sphinx to autogenerate documentation from the docstrings of our code, we can use the `autodoc` extension. 

we have to point Sphinx to the directory in which our Python source codes reside. 
```
sys.path.insert(0, os.path.abspath('../../air_systems'))
print(str(sys.path))
```
**Still not there yet!**  the sphinx.ext.autodoc can only read and understand RST instructions in the comments. We have to use sphinx.ext.napoleon to take our numpydoc docstrings and turn it into RST format that sphinx.ext.autodoc can read.


Now let’s see how we can auto-generate documentation from the docstrings in our Python source files. The `sphinx-apidoc` command can be used to auto-generate some .rst files for our Python module.
 https://sphinx-rtd-tutorial.readthedocs.io/en/latest/build-the-docs.html#generating-documentation-from-docstrings


### sphinx.ext.autosummary
While using sphinx.ext.autodoc makes keeping the code and the documentation in sync much easier, it still requires you to write an auto* (`automodule::`, `autofunction::`, `etc.`) directive for every object you want to document. Sphinx provides yet another level of automation: the **autosummary** extension.

Pay attention to which `*.rst` files have the `.. autosummary::` directive!

### building the html documentation

Run the `Makefile` that comes from using the `sphinx-quickstart` command. This is an
alias for `sphinx-build -b html`. [Citation](https://www.sphinx-doc.org/en/master/man/sphinx-build.html)

```
$ C:\Users\puggy\Documents\GitHub\epug\documentation\web_docs>make clean
$ C:\Users\puggy\Documents\GitHub\epug\documentation\web_docs>make html
```
# An important note for larger repository structures

If you have a complicated repository structure, you may need to explicitly place `__init__.py` files at the level of the subpackage and parent package (e.g., at ./src and at ./src/bpp). Even though `__init__.py` files are no longer required in Python 3.X, Sphinx still uses them to find your modules that you want documented.

# To-do

The fan module autosummary seems to be working. I believe this is because the `fan.py` file doesn't have any import statements that reference something like `src.bpp.air_systems.primary_air_system`.

This ended up not being a sphinx error at all but rather that `import src.bpp.air_systems.primary_air_system` is bad Python.

Absolute versus relative imports

# Additional Reading

Sam Nicholls. [An idiot's guide to Python documentation with Sphinx and Read the Docs](https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/).

Sphinx Maintainers. [Sphinx Quickstart](https://www.sphinx-doc.org/en/master/usage/quickstart.html).

