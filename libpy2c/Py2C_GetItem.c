#include "py2c.h"

// return new reference
PyObject* Py2C_GetItem(PyObject* o, PyObject* key) {
	if (o == NULL) {
		return NULL;
	}
	return PyObject_GetItem(o, key);
}

// return new reference
PyObject* Py2C_GetItemSafe(PyObject* o, PyObject* key) {
	if (o == NULL) {
		return NULL;
	}
	PyObject *retVal = Py2C_GetItem(o, key);
	Py_XDECREF(o);
	return retVal;
}