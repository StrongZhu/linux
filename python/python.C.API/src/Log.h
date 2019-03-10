#ifndef ___LOG_H___
#define ___LOG_H___

#include <stdio.h>
#include <iostream>
#include <thread>
using namespace std;

#define LOG(x)  do { printf x ; cout << " ([" << this_thread::get_id() << "]:" << __FILE__ << ":" << __LINE__ << ")" << endl; } while (0);
// #define LOG(x)  do { } while (0);

#endif
