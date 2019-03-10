from distutils.core import setup, Extension
import os

base_dir = '~/'
if 'BASE_DIR' in os.environ:
  base_dir = os.environ['BASE_DIR']
  pass

foo_module = Extension(
  'foo',

  language = 'c++',

  extra_compile_args = [  '-fPIC',
                          '-std=c++14',
                          '-D _GLIBCXX_USER_CXX11_ABI=0'
  ],

  sources = [ 'src/foo.cpp',
              'src/SessionManager.cpp',
  ],


  include_dirs = [  '~/dir1/',
                    '~/dir2/',
                    base_dir + '/include/',
  ],

  library_dirs = [  '~/lib_dir1/',
                    '~/lib_dir2/',
                    base_dir + '/lib/',
  ],
  
  # libraries = [ 'lib1',
  #               'lib2',
  # ],

  define_macros=  [ ('NDEBUG', '1'),
                  ('HAVE_STRFTIME', None),
                  ],

  undef_macros =  [   'HAVE_FOO', 
                      'HAVE_BAR',
  ],
  
          

)

setup(
  name = 'foo', 
  version = '1.0', 
  description = 'This is a demo package',
  ext_modules = [foo_module],
  )

