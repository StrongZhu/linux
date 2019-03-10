#include <iostream>

using namespace std;


void f(unsigned x, int y)
{
  cout
    << "x=[" << x << "],"
    << "y=[" << y << "],"
    << "x*y=[" << x*y << "],"
    << endl;

}

int main()
{
  f(1, -1);


  // output : 
  //  x=[1],y=[-1],x*y=[4294967295],

  return 0;

}



