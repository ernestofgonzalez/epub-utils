#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "doc.h"
#include <stdlib.h>
#include <string.h>

Document *document_new(const char *path) {
    Document *doc = (Document *)malloc(sizeof(Document));
    if (!doc) {
        fprintf(stderr, "Failed to allocate memory for Document.\n");
        return NULL;
    }
    doc->path = strdup(path);
    return doc;
}

void document_free(Document *doc) {
    if (doc) {
        free(doc->path);
        free(doc);
    }
}

const char *document_get_toc(Document *doc) {
    // For now, return a static TOC string
    return "Chapter 1\nChapter 2\nChapter 3\n";
}

// Document methods
PyObject *Document_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    Document *self;
    self = (Document *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->path = NULL;
    }
    return (PyObject *)self;
}

int Document_init(Document *self, PyObject *args, PyObject *kwds) {
    const char *path;
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return -1;
    }
    self->path = strdup(path);
    if (self->path == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory for path");
        return -1;
    }
    return 0;
}

void Document_dealloc(Document *self) {
    if (self->path) {
        free(self->path);
    }
    Py_TYPE(self)->tp_free((PyObject *)self);
}

PyObject *Document_get_toc(Document *self, PyObject *Py_UNUSED(ignored)) {
    // Return a static TOC string for now
    return PyUnicode_FromString("Chapter 1\nChapter 2\nChapter 3\n");
}

// Document methods table
static PyMethodDef Document_methods[] = {
    {"get_toc", (PyCFunction)Document_get_toc, METH_NOARGS, "Get the Table of Contents"},
    {NULL} // Sentinel
};

// Document type definition
PyTypeObject DocumentType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "doc.Document",
    .tp_doc = "EPUB Document",
    .tp_basicsize = sizeof(Document),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Document_new,
    .tp_init = (initproc)Document_init,
    .tp_dealloc = (destructor)Document_dealloc,
    .tp_methods = Document_methods,
};

// Module methods table
static PyMethodDef module_methods[] = {
    {NULL} // Sentinel
};

// Module definition
static struct PyModuleDef docmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "doc",
    .m_doc = "Module for working with EPUB documents",
    .m_size = -1,
    .m_methods = module_methods,
};

// Module initialization function
PyMODINIT_FUNC PyInit_doc(void) {
    PyObject *m;
    if (PyType_Ready(&DocumentType) < 0) {
        return NULL;
    }
    m = PyModule_Create(&docmodule);
    if (m == NULL) {
        return NULL;
    }
    Py_INCREF(&DocumentType);
    if (PyModule_AddObject(m, "Document", (PyObject *)&DocumentType) < 0) {
        Py_DECREF(&DocumentType);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}
