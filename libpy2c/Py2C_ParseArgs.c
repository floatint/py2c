#include "py2c.h"


// ��������� ������������ ��� �������� ����������
int Py2C_ParseArgs(PyObject* o, Py_ssize_t pos, Py_ssize_t opt, ...) {
	// �������� ������ ������� � �����������
	Py_ssize_t args_size = PyTuple_Size(o);
	// �������� ������ �������
	char *fmt = (char*)malloc(pos + 1);
	fmt[pos] = '\0';
	memset(fmt, 'O', pos);

	if (args_size < pos) {
		PyArg_ParseTuple(o, fmt);
		return NULL;
	}
	else {
		va_list args;
		va_start(args, opt);
		if (args_size < pos + opt) {
			for (int i = 0; i < args_size; i++) {
				*va_arg(args, PyObject**) = PyTuple_GetItem(o, i);
			}
		}
		else {
			for (int i = 0; i < pos + opt; i++) {
				*va_arg(args, PyObject**) = PyTuple_GetItem(o, i);
			}
			PyObject** tuple = va_arg(args, PyObject**);
			*tuple = PyTuple_GetSlice(o, pos + opt, args_size);
		}
		va_end(args);
	}
	free(fmt);
	return 1;
}