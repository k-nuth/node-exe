// Copyright (c) 2016-2020 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef KTH_NODE_EXE_EXECUTOR_HPP_
#define KTH_NODE_EXE_EXECUTOR_HPP_

#include <future>
#include <iostream>
#include <kth/node.hpp>

#include "version.hpp"

namespace kth { namespace node_exe {

class executor {
public:
    executor(kth::node::parser& metadata, std::istream&, std::ostream& output, std::ostream& error);

    /// This class is not copyable.
    executor(executor const&) = delete;
    void operator=(executor const&) = delete;

    /// Invoke the menu command indicated by the metadata.
    bool menu();

private:
    static 
    void stop(kth::code const& ec);
    
    static 
    void handle_stop(int code);

    void handle_started(kth::code const& ec);
    void handle_running(kth::code const& ec);
    void handle_stopped(kth::code const& ec);

    void do_help();
    void do_settings();
    void do_version();
    std::string network_name() const;
    void initialize_output();

#if ! defined(KTH_DB_READONLY)
    bool do_initchain();
#endif // ! defined(KTH_DB_READONLY)    

    bool verify_directory();
    bool run();

    // Termination state.
    static std::promise<kth::code> stopping_;

    kth::node::parser& metadata_;
    std::ostream& output_;
    std::ostream& error_;
    kth::node::full_node::ptr node_;
};

// Localizable messages.
#define KTH_SETTINGS_MESSAGE "These are the configuration settings that can be set."
#define KTH_INFORMATION_MESSAGE "Runs a full bitcoin node with additional client-server query protocol."

#define KTH_UNINITIALIZED_CHAIN "The {} directory is not initialized, run: kth --initchain"
#define KTH_INITIALIZING_CHAIN "Please wait while initializing {} directory..."
#define KTH_INITCHAIN_NEW "Failed to create directory {} with error, '{}'."
#define KTH_INITCHAIN_EXISTS "Failed because the directory {} already exists."
#define KTH_INITCHAIN_TRY "Failed to test directory {} with error, '{}'."
#define KTH_INITCHAIN_COMPLETE "Completed initialization."

#define KTH_NODE_INTERRUPT "Press CTRL-C to stop the node."
#define KTH_NODE_STARTING "Please wait while the node is starting..."
#define KTH_NODE_START_FAIL "Node failed to start with error, {}."
#define KTH_NODE_SEEDED "Seeding is complete."
#define KTH_NODE_STARTED "Node is started."

#define KTH_NODE_SIGNALED "Stop signal detected (code: {})."
#define KTH_NODE_STOPPING "Please wait while the node is stopping..."
#define KTH_NODE_STOP_FAIL "Node failed to stop properly, see log."
#define KTH_NODE_STOPPED "Node stopped successfully."

#define KTH_RPC_STOPPING "RPC-ZMQ service is stopping..."
#define KTH_RPC_STOPPED "RPC-ZMQ service stopped successfully"

#define KTH_USING_CONFIG_FILE "Using config file: {}"

#define KTH_USING_DEFAULT_CONFIG "Using default configuration settings."

#ifdef KTH_WITH_KEOKEN
// Keoken build
#ifdef NDEBUG
#define KTH_VERSION_MESSAGE "Knuth {}\n  currency: {}\n  Keoken Protocol enabled\n  microarchitecture: {}\n  db type: {}"
#else
#define KTH_VERSION_MESSAGE "Knuth {}\n  currency: {}\n  Keoken Protocol enabled\n  microarchitecture: {}\n  db type: {}\n  (Debug Build)"
#endif
#else
// No Keoken build
#ifdef NDEBUG
#define KTH_VERSION_MESSAGE "Knuth v{}\n  currency: {}\n  microarchitecture: {}\n  db type: {}"
#else
#define KTH_VERSION_MESSAGE "Knuth v{}\n  currency: {}\n  microarchitecture: {}\n  db type: {}\n  (Debug Build)"
#endif

#endif

#define KTH_VERSION_MESSAGE_INIT "Node version: {}"

#define KTH_KEOKEN_MESSAGE_INIT "Keoken protocol enabled"

#define KTH_CRYPTOCURRENCY_INIT "Currency: {} - {}"

#define KTH_MICROARCHITECTURE_INIT "Compiled for microarchitecture: {}"

#define KTH_DB_TYPE_INIT "Database type: {}"

#define KTH_DEBUG_BUILD_INIT "(Debug Build)"

#define KTH_NETWORK_INIT "Network: {} ({})"

#define KTH_CORES_INIT "Configured to use {} cores"

// #define KTH_LOG_HEADER "================= startup {} =================="

#if defined(KTH_DB_NEW_FULL)
#define KTH_DB_TYPE "full, new version"
#elif defined(KTH_DB_NEW_BLOCKS)
#define KTH_DB_TYPE "UTXO and Blocks, new version"
#elif defined(KTH_DB_NEW)
#define KTH_DB_TYPE "just UTXO, new version"
#elif defined(KTH_DB_HISTORY)
#define KTH_DB_TYPE "full, legacy version"
#else
#define KTH_DB_TYPE "TXs and Blocks, legacy version"
#endif

}} // namespace kth::node_exe

#endif /*KTH_NODE_EXE_EXECUTOR_HPP_*/
