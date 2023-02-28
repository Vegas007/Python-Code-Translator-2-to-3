# Python-Code-Translator-2-to-3

Is a Python program that reads Python 2.x source code and applies a series of fixers to transform it into valid Python 3.x code ***that work on all versions (py2.x - py3.x).***
The standard library contains a rich set of fixers that will handle almost all code.
A flexible and generic library, so it is possible to write your own fixers based on your purposes.

##### INSTALLATION 

- https://www.python.org/downloads/release/python-391/


##### USING
- Add your .py scripts to the modules folder.
- Run main.bat
- Take the output files and move them into your application.

##### FIXERS

###### print
- Converts the print statement to the print() function.
- Matching multiple formats, comments, and more.

###### Exception handling
- Convert except to except BaseException, since BaseException is the base class for all built-in exceptions.
- Converts except X, T to except X as T.

###### xrange
- Renames xrange() to range() and wraps existing range() calls with list.

###### has_key
- Changed dict.has_key(key) to key in dict

###### dict
- Fixes dictionary iteration methods. dict.iteritems() is converted to dict.items(), dict.iterkeys() to dict.keys(), and dict.itervalues() to dict.values(). 
Similarly, dict.viewitems(), dict.viewkeys() and dict.viewvalues() are converted respectively to dict.items(), dict.keys() and dict.values(). 
It also wraps existing usages of dict.items(), dict.keys(), and dict.values() in a call to list.

###### exec 
- Converts the exec statement to the exec() function.

###### apply
- Removes usage of apply(). For example apply(function, *args, **kwargs) is converted to function(*args, **kwargs).

###### raise
- Converts raise E, V to raise E(V), and raise E, V, T to raise E(V).with_traceback(T). If E is a tuple, the translation will be incorrect because substituting tuples for exceptions has been removed in 3.0.

###### library module names
- Renames the old library names that were renamed with the release of new versions, respecting the latest possible
