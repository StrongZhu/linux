#ifndef ___SESSIONMANAGER_H___
#define ___SESSIONMANAGER_H___

#include <string>
#include <sstream>
#include <thread>
#include <map>

#include "Log.h"

using namespace std;

// ----------------------------------------------
static void Thread_Func(string _topic, PyObject* _callback)
{
  char buf[1024];

  // get current thread id, conver to long
  stringstream ss;
  ss << this_thread::get_id();
  long pid = 0;
  ss >> pid;

  while (1)
  {
    // ------------------------------
    // hold the lock
    PyGILState_STATE state = PyGILState_Ensure();

    // string strTmp;
    // ss >> strTmp;
    // cout << ss.str() << endl;

    sprintf(buf, "*** pid=%ld, _topic=%s ***", pid, _topic.c_str());



    // // both are ok
    //
    // create object
    // PyObject* arglist = Py_BuildValue("lss", pid, _topic.c_str(), buf);

    // create a tuple
    PyObject* arglist = Py_BuildValue("(lss)", pid, _topic.c_str(), buf);


    PyEval_CallObject(_callback, arglist);
    Py_DECREF(arglist);

    // ------------------------------
    // restore the state
    PyGILState_Release(state);

    // ------------------------------
    // sleep for a while
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
  }

  return;
}


// ----------------------------------------------
class SessionManager
{
 public:
  // SessionManager()
  // {
  //   LOG(("SessionManager::SessionManager"));
  // }

  // -----------------
  SessionManager(int _i, double _d, string _s, PyObject* _status_callback)
  {
    m_i = _i;
    m_d = _d;
    m_str = _s;
    m_status_callback = _status_callback;

    // LOG(("SessionManager::SessionManager, [%d][%g][%s]", _i, _d, "_s"));
    LOG(("SessionManager::SessionManager, _i=[%d], _d=[%g], _s[%s]", _i, _d, _s.c_str() ));

    Init();

    if (m_status_callback)
    {
      try
      {
        // increase reference
        Py_INCREF(m_status_callback);
      }
      catch (...)
      {
        LOG(("SessionManager::SessionManager, caught exception..."));
      }
    }
  }

  // -----------------
  ~SessionManager()
  {
    LOG(("SessionManager::~SessionManager"));

    if (m_status_callback)
    {
      try
      {
        // decrease reference
        Py_DECREF(m_status_callback);
      }
      catch (...)
      {
        LOG(("SessionManager::~SessionManager, caught exception..."));
      }
    }
  }

  // -----------------
  // return : sub_id,  ( 0 : failed )
  int Subscribe(string _topic, PyObject* _callback)
  {
    if (!_callback)
      return -1;
   
    // increase reference
    Py_INCREF(_callback);

    m_last_sub_id++;

    m_sub_id_2_callback_map[m_last_sub_id] = _callback;
    m_sub_id_2_topic_map[m_last_sub_id] = _topic;

    thread* pThread = new thread(Thread_Func, _topic, _callback); // pass by value
    m_sub_id_2_pthread_map[m_last_sub_id] = pThread;


    LOG(("SessionManager::Subscribe, m_last_sub_id=[%d], _topic[%s]", m_last_sub_id, _topic.c_str() ));

    return m_last_sub_id;
  }

  // -----------------
  bool UnSubscribe(int _sub_id)
  {
    bool bResult = true;

    if (m_sub_id_2_callback_map.find(_sub_id) != m_sub_id_2_callback_map.end())
    {
      // decrease reference
      Py_DECREF(m_sub_id_2_callback_map[_sub_id]);

      m_sub_id_2_callback_map.erase(_sub_id);
    }
    else
    {
      bResult = false;
    }

    if (m_sub_id_2_topic_map.find(_sub_id) != m_sub_id_2_topic_map.end())
    {
      m_sub_id_2_topic_map.erase(_sub_id);
    }
    else
    {
      bResult = false;
    }

    if (m_sub_id_2_pthread_map.find(_sub_id) != m_sub_id_2_pthread_map.end())
    {
      if (m_sub_id_2_pthread_map[_sub_id])
      {
        m_sub_id_2_pthread_map[_sub_id]->detach();
        LOG(("SessionManager::UnSubscribe, detached : _sub_id=[%d]", _sub_id ));
      }
      m_sub_id_2_pthread_map.erase(_sub_id);
    }
    else
    {
      bResult = false;
    }

    LOG(("SessionManager::UnSubscribe, _sub_id=[%d], bResult=[%d]", _sub_id, bResult ));

    return bResult;
  }
  
  // -----------------
  bool request(string _request)
  {
    LOG(("_request=[%s] : m_sub_id_2_callback_map.size=[%d]", _request.c_str(), m_sub_id_2_callback_map.size() ));
    return true;
  }
  
 protected:
  // -----------------
  void Init()
  {
    m_last_sub_id = 1000;
  } 

 protected:
  int m_i;
  double m_d;
  string m_str;


  PyObject* m_status_callback;

  int m_last_sub_id;
  map<int, PyObject*> m_sub_id_2_callback_map;
  map<int, string> m_sub_id_2_topic_map;
  map<int, thread*> m_sub_id_2_pthread_map;
};

#endif
