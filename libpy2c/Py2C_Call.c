#include "py2c.h"


PyObject* Py2C_Call(PyObject* callable, PyObject* args, PyObject* kwargs) {
	if (callable == NULL) {
		return NULL;
	}
	else {
		return PyObject_Call(callable, args, kwargs);
	}
}