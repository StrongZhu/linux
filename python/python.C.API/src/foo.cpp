#include <Python.h>

#include <iostream>
#include <stdio.h>

#include "foo.h"
#include "SessionManager.h"
#include "Log.h"

using namespace std;

// -----------------------------------------------------------------
static PyObject* foo_bar(PyObject* self, PyObject* args){
  
  cout << "foo_bar" << endl;
  printf("foo_bar\n");
  
  Py_RETURN_NONE;
}

// -----------------------------------------------------------------
static PyObject* foo_bar2(PyObject* self, PyObject* args) {
    int iNum;
    double fNum;
    char* str;
    if (!PyArg_ParseTuple(args, "ids", &iNum, &fNum, &str)) {
        return NULL;
    }
    Py_RETURN_NONE;
}


// -----------------------------------------------------------------
static PyObject* foo_bar3(PyObject* self, PyObject* args, PyObject* kw) {
    static char* kwlist[] = {"i", "d", "s",NULL};
    int iNum = 0;
    double fNum = 2.0f;
    char* str = "thing";
    if (!PyArg_ParseTupleAndKeywords(args,kw,"i|ds",kwlist,&iNum,&fNum,&str)) {
        printf("ERROR");
        return NULL;
    }
    printf("num is: %d,%f,%s\n",iNum,fNum,str);
    Py_RETURN_NONE;
}

// -----------------------------------------------------------------
static PyObject* foo_add_sub(PyObject* self, PyObject* args) {
    int num1,num2;
    if (!PyArg_ParseTuple(args, "ii", &num1, &num2)) {
        return NULL;
    }
    return Py_BuildValue("ii", num1 + num2, num1 - num2);
}

// -----------------------------------------------------------------
extern "C"
PyObject* open_session(PyObject *self, PyObject* args)
{
  // !!! MUST !!!
  // initizlize python, and thread support
  Py_Initialize();
  PyEval_InitThreads();

//   //  ensure we hold the lock
//   PyGILState_STATE gstate = PyGILState_Ensure();

  int i;
  double d;
  const char* pStr;
  PyObject* status_callback;

  // Parsing arguments and building values — Python 2.7.13 documentation.html
  // https://docs.python.org/2/c-api/arg.html
  if (!PyArg_ParseTuple(args, "idsO", &i, &d, &pStr, &status_callback))
  {
    return 0;
  }
  if (!PyCallable_Check(status_callback))
  {
    PyErr_SetString(PyExc_TypeError, "need a callback object"); 
  }

  SessionManager* pSessionManager = 0;
//   pSessionManager = new SessionManager();
  pSessionManager = new SessionManager(i, d, string(pStr), status_callback);

//   // release stats
//   PyGILState_Release(gstate);

  return Py_BuildValue("l", reinterpret_cast<long>(pSessionManager));
}

// -----------------------------------------------------------------
extern "C"
PyObject* close_session(PyObject *self, PyObject* args)
{
  long lSessionManager = 0;
  if (!PyArg_ParseTuple(args, "l", &lSessionManager))
  {
    PyErr_SetString(PyExc_TypeError, "invalid argument type"); 
    return 0;
  }

  SessionManager* pSessionManager = reinterpret_cast<SessionManager*>(lSessionManager);
  if (pSessionManager)
  {
    delete pSessionManager;
  }
  Py_RETURN_NONE;
}

// -----------------------------------------------------------------
extern "C"
PyObject* subscribe(PyObject *self, PyObject* args)
{
  long lSessionManager = 0;
  const char* pTopic;
  PyObject*  callback;

  if (!PyArg_ParseTuple(args, "lsO", &lSessionManager, &pTopic, &callback))
  {
    return 0;
  }
  if (!PyCallable_Check(callback))
  {
    PyErr_SetString(PyExc_TypeError, "need a callback object"); 
  }

  int sub_id = 0;
  SessionManager* pSessionManager = reinterpret_cast<SessionManager*>(lSessionManager);
  if (pSessionManager)
  {
    sub_id = pSessionManager->Subscribe(string(pTopic), callback);
  }

  return Py_BuildValue("i", sub_id);
}

// -----------------------------------------------------------------
extern "C"
PyObject* unsubscribe(PyObject *self, PyObject* args)
{
  long lSessionManager = 0;
  int sub_id;

  if (!PyArg_ParseTuple(args, "li", &lSessionManager, &sub_id))
  {
    return 0;
  }

  SessionManager* pSessionManager = reinterpret_cast<SessionManager*>(lSessionManager);
  bool result = false;
  if (pSessionManager)
  {
    result = pSessionManager->UnSubscribe(sub_id);
  }

  return Py_BuildValue("i", result);
}

// -----------------------------------------------------------------
extern "C"
PyObject* request(PyObject *self, PyObject* args)
{
  long lSessionManager = 0;
  const char* pRequest;

  if (!PyArg_ParseTuple(args, "ls", &lSessionManager, &pRequest))
  {
    return 0;
  }

  SessionManager* pSessionManager = reinterpret_cast<SessionManager*>(lSessionManager);
  bool result = false;
  if (pSessionManager)
  {
    result = pSessionManager->request(string(pRequest));
  }

  return Py_BuildValue("i", result);
}


// -----------------------------------------------------------------
static PyMethodDef foo_methods[] = {
    {"bar",(PyCFunction)foo_bar,METH_NOARGS,NULL},
    {"bar2", (PyCFunction)foo_bar2,METH_VARARGS,NULL},
    {"bar3", (PyCFunction)foo_bar3, METH_VARARGS|METH_KEYWORDS, NULL},
    {"add_sub", (PyCFunction)foo_add_sub, METH_VARARGS, NULL},

    {"open_session", (PyCFunction)open_session, METH_VARARGS, NULL},
    {"close_session", (PyCFunction)close_session, METH_VARARGS, NULL},

    {"subscribe", (PyCFunction)subscribe, METH_VARARGS, NULL},
    {"unsubscribe", (PyCFunction)unsubscribe, METH_VARARGS, NULL},

    {"request", (PyCFunction)request, METH_VARARGS, NULL},
    
    {NULL,NULL,0,NULL}
};

// -----------------------------------------------------------------
PyMODINIT_FUNC initfoo() {
  //Py_InitModule3("foo", foo_methods, "My first extension module.");
  Py_InitModule("foo", foo_methods);
}
