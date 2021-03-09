#include "py2c.h"

// return new reference
PyObject* Py2C_GetAttrString(PyObject *o, const char* attr_name) {
	if (o == NULL) {
		return NULL;
	}
	return PyObject_GetAttrString(o, attr_name);
}

// return new reference
PyObject* Py2C_GetAttrStringSafe(PyObject *o, const char* attr_name) {
	if (o == NULL) {
		return NULL;
	}
	PyObject *attr = Py2C_GetAttrString(o, attr_name);
	Py_XDECREF(o);
	return attr;
}