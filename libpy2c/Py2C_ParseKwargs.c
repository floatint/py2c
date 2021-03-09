#include "py2c.h"
#include <stdio.h>


// Системная функция для парсинга keyword аргументов
// keywords - массив ключей с NULL в конце
int Py2C_ParseKwargs(PyObject* kwargs, const char *keywords[], ...) {
	if (keywords == NULL) {
		return NULL;
	}

	int keywordsSize = 0;

	while (keywords[keywordsSize++] != NULL) {
	}

	va_list kwlist;
	va_start(kwlist, keywords);
	PyObject* kws = PyDict_New();

	for (int i = 0; i < keywordsSize - 1; i++) {
		PyObject* strObj = PyUnicode_FromString(keywords[i]);
		if (PyDict_Contains(kwargs, strObj)) {
			*va_arg(kwlist, PyObject**) = PyDict_GetItemString(kwargs, keywords[i]);
			PyDict_DelItem(kwargs, strObj);
		}
		else {
			PyDict_SetItemString(kws, keywords[i], PyDict_GetItemString(kwargs, keywords[i]));
		}
		Py_DECREF(strObj);
	}

	Py_ssize_t pos = 0;
	PyObject *key = NULL;
	PyObject *value = NULL;
	while (PyDict_Next(kwargs, &pos, &key, &value)) {
		PyDict_SetItem(kws, key, value);
	}

	*va_arg(kwlist, PyObject**) = kws;

	return 1;
}