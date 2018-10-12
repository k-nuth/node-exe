mkdir build
cd build
# rm -rf *
# rm -rf bin
conan install .. -o use_domain=False -o db_transaction_unconfirmed=False -o db_spends=False -o db_history=False -o db_stealth=False -o db_unspent_libbitcoin=False -o db_legacy=False -o db_new=True -s build_type=Debug
# conan install .. -o use_domain=False -o db_transaction_unconfirmed=False -o db_spends=False -o db_history=False -o db_stealth=False -o db_unspent_libbitcoin=False -o db_legacy=False -o db_new=True -s build_type=Release
conan build ..