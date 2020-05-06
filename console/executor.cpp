// Copyright (c) 2016-2020 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include "executor.hpp"

#include <csignal>
#include <functional>
#include <future>
#include <iostream>
#include <memory>
#include <mutex>

#include <boost/core/null_deleter.hpp>

#include <kth/domain/multi_crypto_support.hpp>
#include <kth/node.hpp>


#ifdef KTH_WITH_RPC
#include <kth/rpc/manager.hpp>
#include <unordered_set>
#endif

namespace kth::node_exe {

// using boost::format;
using namespace boost;
using namespace boost::system;
using namespace bc::chain;
using namespace bc::config;
using namespace bc::database;
using namespace bc::network;
using namespace std::placeholders;

static auto const application_name = "kth";
static constexpr int initialize_stop = 0;
static constexpr int directory_exists = 0;
static constexpr int directory_not_found = 2;
static auto const mode = std::ofstream::out | std::ofstream::app;

std::promise<kth::code> executor::stopping_;

executor::executor(kth::node::parser& metadata, std::istream& input, std::ostream& output, std::ostream& error)
    : metadata_(metadata), output_(output), error_(error)
{
    auto const& network = metadata_.configured.network;
    auto const verbose = network.verbose;

#if defined(KTH_LOG_LIBRARY_BOOST)
    kth::log::rotable_file const debug_file {
        network.debug_file,
        network.archive_directory,
        network.rotation_size,
        network.maximum_archive_size,
        network.minimum_free_space,
        network.maximum_archive_files
    };

    kth::log::rotable_file const error_file {
        network.error_file,
        network.archive_directory,
        network.rotation_size,
        network.maximum_archive_size,
        network.minimum_free_space,
        network.maximum_archive_files
    };
#elif defined(DKTH_LOG_LIBRARY_SPDLOG)
#else
#endif


#if defined(KTH_STATISTICS_ENABLED)
    kth::log::initialize(debug_file, error_file, verbose);
#else

#if defined(KTH_LOG_LIBRARY_BOOST)
    kth::log::stream console_out(&output_, null_deleter());
    kth::log::stream console_err(&error_, null_deleter());
    kth::log::initialize(debug_file, error_file, console_out, console_err, verbose);
#else
#endif

#endif

    handle_stop(initialize_stop);
}

// Command line options.
// ----------------------------------------------------------------------------
// Emit directly to standard output (not the log).

void executor::do_help() {
    auto const options = metadata_.load_options();
    printer help(options, application_name, KTH_INFORMATION_MESSAGE);
    help.initialize();
    help.commandline(output_);
}

void executor::do_settings() {
    auto const settings = metadata_.load_settings();
    printer print(settings, application_name, KTH_SETTINGS_MESSAGE);
    print.initialize();
    print.settings(output_);
}

void executor::do_version() {
    output_ << fmt::format(KTH_VERSION_MESSAGE, KTH_NODE_EXE_VERSION, KTH_CURRENCY_SYMBOL_STR, KTH_MICROARCHITECTURE_STR, KTH_DB_TYPE) << std::endl;
}

#if ! defined(KTH_DB_READONLY)
// Emit to the log.
bool executor::do_initchain() {
    initialize_output();

    error_code ec;
    auto const& directory = metadata_.configured.database.directory;

    if (create_directories(directory, ec)) {
        LOG_INFO(LOG_NODE, fmt::format(KTH_INITIALIZING_CHAIN, directory.string()));
        auto const genesis = kth::node::full_node::get_genesis_block(metadata_.configured.chain);
        auto const& settings = metadata_.configured.database;
        auto const result = data_base(settings).create(genesis);
        LOG_INFO(LOG_NODE, KTH_INITCHAIN_COMPLETE);
        return result;
    }

    if (ec.value() == directory_exists) {
        LOG_ERROR(LOG_NODE, fmt::format(KTH_INITCHAIN_EXISTS, directory.string()));
        return false;
    }

    LOG_ERROR(LOG_NODE, fmt::format(KTH_INITCHAIN_NEW, directory.string(), ec.message()));
    return false;
}
#endif // ! defined(KTH_DB_READONLY)

// Menu selection.
// ----------------------------------------------------------------------------

bool executor::menu() {
    auto const& config = metadata_.configured;

    if (config.help) {
        do_help();
        return true;
    }

    if (config.settings) {
        do_settings();
        return true;
    }

    if (config.version) {
        do_version();
        return true;
    }

#if ! defined(KTH_DB_READONLY)
    if (config.initchain) {
        return do_initchain();
    }
#endif // ! defined(KTH_DB_READONLY)    

    // There are no command line arguments, just run the node.
    return run();
}

// Run.
// ----------------------------------------------------------------------------

bool executor::run() {
    initialize_output();

    LOG_INFO(LOG_NODE, KTH_NODE_INTERRUPT);
    LOG_INFO(LOG_NODE, KTH_NODE_STARTING);

    //Log Cryotocurrency
    //Log Microarchitecture
    if ( ! verify_directory()) {
        return false;
    }

    bool const testnet = kth::get_network(metadata_.configured.network.identifier) == kth::config::settings::testnet;

    metadata_.configured.node.testnet = testnet;

    // Now that the directory is verified we can create the node for it.
    node_ = std::make_shared<kth::node::full_node>(metadata_.configured);

#if defined(KTH_LOG_LIBRARY_BOOST)
    // Initialize broadcast to statistics server if configured.
    kth::log::initialize_statsd(node_->thread_pool(), metadata_.configured.network.statistics_server);
#else
    //TODO(fernando): implement this for spdlog and binlog
#endif


    // The callback may be returned on the same thread.
    node_->start(std::bind(&executor::handle_started, this, _1));

#ifdef KTH_WITH_RPC
    std::string message = "RPC port: " + std::to_string(metadata_.configured.node.rpc_port) + ". ZMQ port: " + std::to_string(metadata_.configured.node.subscriber_port);
    LOG_INFO(LOG_NODE, message);
    if (metadata_.configured.node.rpc_allow_all_ips) {
        LOG_INFO(LOG_NODE, "RPC is listening requests from all addresses");
    }

    std::unordered_set<std::string> rpc_allowed_ips;
    
    for (auto const& ip : metadata_.configured.node.rpc_allow_ip) {
        rpc_allowed_ips.insert(ip);
    }

#ifdef KTH_WITH_KEOKEN
    kth::rpc::manager message_manager (metadata_.configured.node.testnet, *node_, metadata_.configured.node.rpc_port, metadata_.configured.node.subscriber_port, metadata_.configured.node.keoken_genesis_height, rpc_allowed_ips, metadata_.configured.node.rpc_allow_all_ips);
#else
    kth::rpc::manager message_manager (metadata_.configured.node.testnet, *node_, metadata_.configured.node.rpc_port, metadata_.configured.node.subscriber_port, rpc_allowed_ips, metadata_.configured.node.rpc_allow_all_ips);
#endif
    
    auto rpc_thread = std::thread([&message_manager]() {
        message_manager.start();
    });
#endif

    // Wait for stop.
    stopping_.get_future().wait();

    LOG_INFO(LOG_NODE, KTH_NODE_STOPPING);

#ifdef KTH_WITH_RPC
    if (!message_manager.is_stopped()) {
        LOG_INFO(LOG_NODE, KTH_RPC_STOPPING);
        message_manager.stop();
        rpc_thread.join();
        LOG_INFO(LOG_NODE, KTH_RPC_STOPPED);
    }
#endif

    // Close must be called from main thread.
    if (node_->close()) {
        LOG_INFO(LOG_NODE, KTH_NODE_STOPPED);
    } else {
        LOG_INFO(LOG_NODE, KTH_NODE_STOP_FAIL);
    }

    return true;
}

// Handle the completion of the start sequence and begin the run sequence.
void executor::handle_started(kth::code const& ec) {
    if (ec) {
        LOG_ERROR(LOG_NODE, fmt::format(KTH_NODE_START_FAIL, ec.message()));
        stop(ec);
        return;
    }

    LOG_INFO(LOG_NODE, KTH_NODE_SEEDED);

    // This is the beginning of the stop sequence.
    node_->subscribe_stop(std::bind(&executor::handle_stopped, this, _1));

    // This is the beginning of the run sequence.
    node_->run(std::bind(&executor::handle_running, this, _1));
}

// This is the end of the run sequence.
void executor::handle_running(kth::code const& ec) {
    if (ec) {
        LOG_INFO(LOG_NODE, fmt::format(KTH_NODE_START_FAIL, ec.message()));
        stop(ec);
        return;
    }

    LOG_INFO(LOG_NODE, KTH_NODE_STARTED);
}

// This is the end of the stop sequence.
void executor::handle_stopped(kth::code const& ec) {
    stop(ec);
}

// Stop signal.
// ----------------------------------------------------------------------------

void executor::handle_stop(int code) {
    // Reinitialize after each capture to prevent hard shutdown.
    // Do not capture failure signals as calling stop can cause flush lock file
    // to clear due to the aborted thread dropping the flush lock mutex.
    std::signal(SIGINT, handle_stop);
    std::signal(SIGTERM, handle_stop);

    if (code == initialize_stop) {
        return;
    }

    LOG_INFO(LOG_NODE, fmt::format(KTH_NODE_SIGNALED, code));
    stop(kth::error::success);
}

// Manage the race between console stop and server stop.
void executor::stop(kth::code const& ec) {
    static std::once_flag stop_mutex;
    std::call_once(stop_mutex, [&](){ stopping_.set_value(ec); });
}

// Utilities.
// ----------------------------------------------------------------------------

std::string executor::network_name() const {
    switch (kth::get_network(metadata_.configured.network.identifier)) {
        case kth::config::settings::testnet:
            return "Testnet";
        case kth::config::settings::mainnet:
            return "Mainnet";
        case kth::config::settings::regtest:
            return "Regtest";
    }
    return "Unknown";
}

// Set up logging.
void executor::initialize_output() {
    // auto const header = fmt::format(KTH_LOG_HEADER, kth::local_time());
    // LOG_DEBUG(LOG_NODE, header);
    // LOG_INFO(LOG_NODE, header);
    // LOG_WARNING(LOG_NODE, header);
    // LOG_ERROR(LOG_NODE, header);
    // LOG_FATAL(LOG_NODE, header);

    auto const& file = metadata_.configured.file;

    if (file.empty()) {
        LOG_INFO(LOG_NODE, KTH_USING_DEFAULT_CONFIG);
    } else {
        LOG_INFO(LOG_NODE, fmt::format(KTH_USING_CONFIG_FILE, file.string()));
    }

    LOG_INFO(LOG_NODE, fmt::format(KTH_VERSION_MESSAGE_INIT, KTH_NODE_EXE_VERSION));
    LOG_INFO(LOG_NODE, fmt::format(KTH_CRYPTOCURRENCY_INIT, KTH_CURRENCY_SYMBOL_STR, KTH_CURRENCY_STR));

#ifdef KTH_WITH_KEOKEN
    LOG_INFO(LOG_NODE, fmt::format(KTH_KEOKEN_MESSAGE_INIT));
#endif

    LOG_INFO(LOG_NODE, fmt::format(KTH_MICROARCHITECTURE_INIT, KTH_MICROARCHITECTURE_STR));

    LOG_INFO(LOG_NODE, fmt::format(KTH_DB_TYPE_INIT, KTH_DB_TYPE));


#ifndef NDEBUG
    LOG_INFO(LOG_NODE, KTH_DEBUG_BUILD_INIT);
#endif

    LOG_INFO(LOG_NODE, fmt::format(KTH_NETWORK_INIT, network_name(), metadata_.configured.network.identifier));
    LOG_INFO(LOG_NODE, fmt::format(KTH_CORES_INIT, kth::thread_ceiling(metadata_.configured.chain.cores)));
}

// Use missing directory as a sentinel indicating lack of initialization.
bool executor::verify_directory() {
    error_code ec;
    auto const& directory = metadata_.configured.database.directory;

    if (exists(directory, ec)) {
        return true;
    }

    if (ec.value() == directory_not_found) {
        LOG_ERROR(LOG_NODE, fmt::format(KTH_UNINITIALIZED_CHAIN, directory.string()));
        return false;
    }

    auto const message = ec.message();
    LOG_ERROR(LOG_NODE, fmt::format(KTH_INITCHAIN_TRY, directory.string(), message));
    return false;
}

} // namespace kth::node_exe