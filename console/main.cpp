// Copyright (c) 2016-2020 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.



#include <cstdio>
#include <iostream>

#include <kth/node.hpp>
#include <boost/iostreams/device/file_descriptor.hpp>
#include "executor.hpp"

KTH_USE_MAIN

int kth::main(int argc, char* argv[]) {
    using namespace bc;
    using namespace bc::node;
    using namespace kth;
    using namespace kth::node_exe;

    set_utf8_stdio();
    auto const& args = const_cast<const char**>(argv);

    node::parser metadata(kth::config::settings::mainnet);
    if ( ! metadata.parse(argc, args, cerr)) {
        return console_result::failure;
    }

    executor host(metadata, cin, cout, cerr);
    return host.menu() ? console_result::okay : console_result::failure;
}
