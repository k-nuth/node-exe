/**
 * Copyright (c) 2017-2018 Bitprim Inc.
 *
 * This file is part of Bitprim.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


#include <cstdio>
#include <iostream>

#include <bitcoin/node.hpp>
#include <boost/iostreams/device/file_descriptor.hpp>
#include "executor.hpp"

BC_USE_LIBBITCOIN_MAIN

int bc::main(int argc, char* argv[]) {
    using namespace bc;
    using namespace bc::node;
    using namespace bitprim;
    using namespace bitprim::node_exe;

    set_utf8_stdio();
    const auto& args = const_cast<const char**>(argv);

    node::parser metadata(libbitcoin::config::settings::mainnet);
    if ( ! metadata.parse(argc, args, cerr)) {
        return console_result::failure;
    }

    executor host(metadata, cin, cout, cerr);
    return host.menu() ? console_result::okay : console_result::failure;
}
