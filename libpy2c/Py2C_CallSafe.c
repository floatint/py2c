#include "py2c.h"


PyObject* Py2C_CallSafe(PyObject* callable, PyObject* args, PyObject* kwargs) {
	if (callable == NULL) {
		return NULL;
	}
	else {
		PyObject* tmp = PyObject_Call(callable, args, kwargs);
		Py_DECREF(callable);
		return tmp;
	}

}