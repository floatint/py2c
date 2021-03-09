#ifndef PY_2_C
#define PY_2_C

/*

	Py2C translator useful functions library.

*/

#include <Python.h>
#include "structmember.h"

/*
 *	Parse arguments (positional and optional)
 *
 *	@param args Tuple of arguments
 *	@param pos Count of positional arguments
 *	@param opt Count of optional arguments
 *	@param ... List of references to arguments
 *	@return 0 - error with exception setting, 1 - successful
 */
int Py2C_ParseArgs(PyObject* args, Py_ssize_t pos, Py_ssize_t opt, ...);
/*
 *	Parse keyword arguments
 *
 *	@param kwargs Keyword arguments dictionary
 *	@param kwnames Array of names of keyword arguments
 *	@param ... List of references to arguments
 *	@return 0 - error with setting exception, 1 - successful
 */
int Py2C_ParseKwargs(PyObject *kwargs, const char *kwnames[], ...);
/*
 *	Get object's attrubute by his string name
 *	Note ! Return new reference
 *
 *	@param o Target object
 *	@param attr_name Attribute name
 *	@return NULL - error with setting exception, else - attribute object
 */
PyObject* Py2C_GetAttrString(PyObject* o, const char* attr_name);
/*
 *	Get object's attrubute by his string name with decreasing @param o ref counter
 *	Note ! Return new reference
 *
 *	@param o Target object
 *	@param attr_name Attribute name
 *	@return NULL - error with setting exception, else - attribute object
 */
PyObject* Py2C_GetAttrStringSafe(PyObject* o, const char* attr_name);
int Py2C_SetAttrString(PyObject* o, const char* attr_name, PyObject* v);
int Py2C_SetAttrStringSafe(PyObject* o, const char* attr_name, PyObject* v);
PyObject* Py2C_GetItem(PyObject* o, PyObject* key);
PyObject* Py2C_GetItemSafe(PyObject* o, PyObject* key);
int Py2C_SetItem(PyObject* o, PyObject* key, PyObject* v);

#endif // !PY_2_C
