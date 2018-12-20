mkdir build
cd build
conan install ..  -o use_domain=False -o db=new_full -o *:keoken=True -s build_type=Debug
conan build ..