#ifndef DOCUMENT_H
#define DOCUMENT_H

#include <Python.h>

typedef struct {
    PyObject_HEAD
    char *path;
} Document;

PyObject *Document_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
int Document_init(Document *self, PyObject *args, PyObject *kwds);
void Document_dealloc(Document *self);
PyObject *Document_get_toc(Document *self, PyObject *Py_UNUSED(ignored));

extern PyTypeObject DocumentType;

PyMODINIT_FUNC PyInit_doc(void);

#endif // DOCUMENT_H
