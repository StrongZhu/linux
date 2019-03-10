# # OLD way to build
# export CXX_PARAM="-shared -fPIC -I /usr/include/python2.7/"
# g++ ${CXX_PARAM}  src/foo.cpp -o foo.so


# build
python ./setup.py build       $*
# python ./setup.py build -f -g

# install
# python ./setup.py install --prefix=./


