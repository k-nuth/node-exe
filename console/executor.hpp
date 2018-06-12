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
#ifndef BITPRIM_NODE_EXE_EXECUTOR_HPP_
#define BITPRIM_NODE_EXE_EXECUTOR_HPP_

#include <future>
#include <iostream>
#include <bitcoin/node.hpp>

#include "version.hpp"

namespace bitprim { namespace node_exe {

class executor {
public:
    executor(libbitcoin::node::parser& metadata, std::istream&, std::ostream& output, std::ostream& error);

    /// This class is not copyable.
    executor(executor const&) = delete;
    void operator=(executor const&) = delete;

    /// Invoke the menu command indicated by the metadata.
    bool menu();

private:
    static 
    void stop(libbitcoin::code const& ec);
    
    static 
    void handle_stop(int code);

    void handle_started(libbitcoin::code const& ec);
    void handle_running(libbitcoin::code const& ec);
    void handle_stopped(libbitcoin::code const& ec);

    void do_help();
    void do_settings();
    void do_version();
    std::string network_name() const;
    void initialize_output();

#if !defined(WITH_REMOTE_BLOCKCHAIN) && !defined(WITH_REMOTE_DATABASE)
    bool do_initchain();
    bool verify_directory();
#endif    

    bool run();

    // Termination state.
    static std::promise<libbitcoin::code> stopping_;

    libbitcoin::node::parser& metadata_;
    std::ostream& output_;
    std::ostream& error_;
    libbitcoin::node::full_node::ptr node_;
};

// Localizable messages.
#define BN_SETTINGS_MESSAGE \
    "These are the configuration settings that can be set."
#define BN_INFORMATION_MESSAGE \
    "Runs a full bitcoin node with additional client-server query protocol."

#if !defined(WITH_REMOTE_BLOCKCHAIN) && !defined(WITH_REMOTE_DATABASE)
#define BN_UNINITIALIZED_CHAIN \
    "The %1% directory is not initialized, run: bn --initchain"
#define BN_INITIALIZING_CHAIN \
    "Please wait while initializing %1% directory..."
#define BN_INITCHAIN_NEW \
    "Failed to create directory %1% with error, '%2%'."
#define BN_INITCHAIN_EXISTS \
    "Failed because the directory %1% already exists."
#define BN_INITCHAIN_TRY \
    "Failed to test directory %1% with error, '%2%'."
#define BN_INITCHAIN_COMPLETE \
    "Completed initialization."
#endif // !defined(WITH_REMOTE_BLOCKCHAIN) && !defined(WITH_REMOTE_DATABASE)

#define BN_NODE_INTERRUPT \
    "Press CTRL-C to stop the node."
#define BN_NODE_STARTING \
    "Please wait while the node is starting..."
#define BN_NODE_START_FAIL \
    "Node failed to start with error, %1%."
#define BN_NODE_SEEDED \
    "Seeding is complete."
#define BN_NODE_STARTED \
    "Node is started."

#define BN_NODE_SIGNALED \
    "Stop signal detected (code: %1%)."
#define BN_NODE_STOPPING \
    "Please wait while the node is stopping..."
#define BN_NODE_STOP_FAIL \
    "Node failed to stop properly, see log."
#define BN_NODE_STOPPED \
    "Node stopped successfully."

#define BN_RPC_STOPPING \
    "RPC-ZMQ service is stopping..."
#define BN_RPC_STOPPED \
    "RPC-ZMQ service stopped successfully"

#define BN_USING_CONFIG_FILE \
    "Using config file: %1%"

#define BN_USING_DEFAULT_CONFIG \
    "Using default configuration settings."

#ifdef NDEBUG
#define BN_VERSION_MESSAGE "Bitprim %1%\n  currency: %2%\n  microarchitecture: %3%"
#else
#define BN_VERSION_MESSAGE "Bitprim %1%\n  currency: %2%\n  microarchitecture: %3%\n  (Debug Build)"
#endif

#define BN_VERSION_MESSAGE_INIT "Node version: %1%"

#define BN_CRYPTOCURRENCY_INIT "Currency: %1% - %2%"

#define BN_MICROARCHITECTURE_INIT "Compiled for microarchitecture: %1%"

#define BN_DEBUG_BUILD_INIT "(Debug Build)"

#define BN_NETWORK_INIT "Network: %1% (%2%)"


#define BN_LOG_HEADER \
    "================= startup %1% =================="


// #ifdef BITPRIM_BUILD_NUMBER
// #define BITPRIM_NODE_EXE_VERSION BITPRIM_BUILD_NUMBER
// #else
// #define BITPRIM_NODE_EXE_VERSION "v0.0.0"
// #endif

}} // namespace bitprim::node_exe

#endif /*BITPRIM_NODE_EXE_EXECUTOR_HPP_*/
