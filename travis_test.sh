#!/bin/bash
source scl_source enable devtoolset-7
source loadLSST.bash
pip install nose
pip install coveralls
eups declare cp_pipe_drivers -r ${TRAVIS_BUILD_DIR} -t current
setup cp_pipe_drivers
cd ${TRAVIS_BUILD_DIR}
scons opt=3
nosetests -s --with-coverage --cover-package=desc.cp_pipe_drivers
