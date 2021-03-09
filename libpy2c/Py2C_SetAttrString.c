#include "py2c.h"

int Py2C_SetAttrString(PyObject* o, const char* attr_name, PyObject* v) {
	if (o == NULL) {
		return NULL;
	}
	return PyObject_SetAttrString(o, attr_name, v);
}

int Py2C_SetAttrStringSafe(PyObject* o, const char* attr_name, PyObject* v) {
	if (o == NULL) {
		return NULL;
	}
	int retVal = Py2C_SetAttrString(o, attr_name, v);
	Py_XDECREF(o);
	return retVal;
}