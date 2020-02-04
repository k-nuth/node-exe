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

#if !defined(WITH_REMOTE_BLOCKCHAIN) && !defined(WITH_REMOTE_DATABASE)
    bool do_initchain();
    bool verify_directory();
#endif    

    bool run();

    // Termination state.
    static std::promise<kth::code> stopping_;

    kth::node::parser& metadata_;
    std::ostream& output_;
    std::ostream& error_;
    kth::node::full_node::ptr node_;
};

// Localizable messages.
#define KTH_SETTINGS_MESSAGE \
    "These are the configuration settings that can be set."
#define KTH_INFORMATION_MESSAGE \
    "Runs a full bitcoin node with additional client-server query protocol."

#if !defined(WITH_REMOTE_BLOCKCHAIN) && !defined(WITH_REMOTE_DATABASE)
#define KTH_UNINITIALIZED_CHAIN \
    "The %1% directory is not initialized, run: kth --initchain"
#define KTH_INITIALIZING_CHAIN \
    "Please wait while initializing %1% directory..."
#define KTH_INITCHAIN_NEW \
    "Failed to create directory %1% with error, '%2%'."
#define KTH_INITCHAIN_EXISTS \
    "Failed because the directory %1% already exists."
#define KTH_INITCHAIN_TRY \
    "Failed to test directory %1% with error, '%2%'."
#define KTH_INITCHAIN_COMPLETE \
    "Completed initialization."
#endif // !defined(WITH_REMOTE_BLOCKCHAIN) && !defined(WITH_REMOTE_DATABASE)

#define KTH_NODE_INTERRUPT \
    "Press CTRL-C to stop the node."
#define KTH_NODE_STARTING \
    "Please wait while the node is starting..."
#define KTH_NODE_START_FAIL \
    "Node failed to start with error, %1%."
#define KTH_NODE_SEEDED \
    "Seeding is complete."
#define KTH_NODE_STARTED \
    "Node is started."

#define KTH_NODE_SIGNALED \
    "Stop signal detected (code: %1%)."
#define KTH_NODE_STOPPING \
    "Please wait while the node is stopping..."
#define KTH_NODE_STOP_FAIL \
    "Node failed to stop properly, see log."
#define KTH_NODE_STOPPED \
    "Node stopped successfully."

#define KTH_RPC_STOPPING \
    "RPC-ZMQ service is stopping..."
#define KTH_RPC_STOPPED \
    "RPC-ZMQ service stopped successfully"

#define KTH_USING_CONFIG_FILE \
    "Using config file: %1%"

#define KTH_USING_DEFAULT_CONFIG \
    "Using default configuration settings."

#ifdef KTH_WITH_KEOKEN
// Keoken build
#ifdef NDEBUG
#define KTH_VERSION_MESSAGE "Knuth %1%\n  currency: %2%\n  Keoken Protocol enabled\n  microarchitecture: %3%\n  db type: %4%"
#else
#define KTH_VERSION_MESSAGE "Knuth %1%\n  currency: %2%\n  Keoken Protocol enabled\n  microarchitecture: %3%\n  db type: %4%\n  (Debug Build)"
#endif
#else
// No Keoken build
#ifdef NDEBUG
#define KTH_VERSION_MESSAGE "Knuth v%1%\n  currency: %2%\n  microarchitecture: %3%\n  db type: %4%"
#else
#define KTH_VERSION_MESSAGE "Knuth v%1%\n  currency: %2%\n  microarchitecture: %3%\n  db type: %4%\n  (Debug Build)"
#endif

#endif

#define KTH_VERSION_MESSAGE_INIT "Node version: %1%"

#define KTH_KEOKEN_MESSAGE_INIT "Keoken protocol enabled"

#define KTH_CRYPTOCURRENCY_INIT "Currency: %1% - %2%"

#define KTH_MICROARCHITECTURE_INIT "Compiled for microarchitecture: %1%"

#define KTH_DB_TYPE_INIT "Database type: %1%"

#define KTH_DEBUG_BUILD_INIT "(Debug Build)"

#define KTH_NETWORK_INIT "Network: %1% (%2%)"

#define KTH_CORES_INIT "Configured to use %1% cores"

#define KTH_LOG_HEADER \
    "================= startup %1% =================="

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
