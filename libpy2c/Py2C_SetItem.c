#include "py2c.h"


int Py2C_SetItem(PyObject* o, PyObject* key, PyObject* v) {
	return PyObject_SetItem(o, key, v);
}