mkdir build
cd build

# rm -rf *
# conan install .. -o db=legacy_full -o use_domain=False -s build_type=Debug
conan install .. -o db=new -o use_domain=False -s build_type=Debug

conan build ..