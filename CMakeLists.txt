#
# Copyright (c) 2017-2018 Bitprim Inc.
#
# This file is part of Bitprim.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

cmake_minimum_required(VERSION 3.4)

# bitprim-node-exe
#==============================================================================
project(bitprim-node-exe
        VERSION 0
        LANGUAGES CXX C)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Check for baseline language coverage in the compiler for the C++14 standard.
#------------------------------------------------------------------------------
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Process options.
#==============================================================================

# Implement --use-conan
#------------------------------------------------------------------------------
option(USE_CONAN "Use Conan Build Tool." OFF)
option(NO_CONAN_AT_ALL "Conan totally disabled." OFF)

# Implement --with_rpc
#------------------------------------------------------------------------------
option(WITH_RPC "Compile with RPC-ZMQ support." OFF)
if (WITH_RPC)
  add_definitions(-DBITPRIM_WITH_RPC)
endif()

if (NO_CONAN_AT_ALL)
  set(USE_CONAN OFF)
endif()

set(BITPRIM_PROJECT_VERSION "-" CACHE STRING "Specify the Bitprim Project Version.")
# message(${BITPRIM_PROJECT_VERSION})
message( STATUS "Bitprim: Compiling version ${BITPRIM_PROJECT_VERSION}")

set(MICROARCHITECTURE "x86_64" CACHE STRING "Specify the Cryptocurrency (x86_64|...).")
message( STATUS "Bitprim: Compiling for ${MICROARCHITECTURE}")
add_definitions(-DBITPRIM_MICROARCHITECTURE=${MICROARCHITECTURE})
add_definitions(-DBITPRIM_MICROARCHITECTURE_STR="${MICROARCHITECTURE}")

set(CURRENCY "BCH" CACHE STRING "Specify the Cryptocurrency (BCH|BTC|LTC).")

if (${CURRENCY} STREQUAL "BCH")
  add_definitions(-DBITPRIM_CURRENCY_BCH)
  add_definitions(-DBITPRIM_CURRENCY_SYMBOL_STR="BCH")
  add_definitions(-DBITPRIM_CURRENCY_STR="Bitcoin Cash")
elseif (${CURRENCY} STREQUAL "BTC")
  add_definitions(-DBITPRIM_CURRENCY_BTC)
  add_definitions(-DBITPRIM_CURRENCY_SYMBOL_STR="BTC")
  add_definitions(-DBITPRIM_CURRENCY_STR="Bitcoin Legacy")
elseif (${CURRENCY} STREQUAL "LTC")
  add_definitions(-DBITPRIM_CURRENCY_LTC)
  add_definitions(-DBITPRIM_CURRENCY_SYMBOL_STR="LTC")
  add_definitions(-DBITPRIM_CURRENCY_STR="Litecoin")
else()
  message(FATAL_ERROR "Invalid Cryptocurrency: ${CURRENCY}")
endif()

message(STATUS "Bitprim: Cryptocurrency: ${CURRENCY}")

# Implement --with-keoken and declare WITH_KEOKEN.
#------------------------------------------------------------------------------
option(WITH_KEOKEN "Keoken enabled." OFF)
if (WITH_KEOKEN)
  message(STATUS "Bitprim: Keoken enabled")
  add_definitions(-DBITPRIM_WITH_KEOKEN)
endif()

# Implement --with-mempool and declare WITH_MEMPOOL.
#------------------------------------------------------------------------------
option(WITH_MEMPOOL "Mempool enabled." OFF)
if (WITH_MEMPOOL)
  message(STATUS "Bitprim: Mempool enabled")
  add_definitions(-DBITPRIM_WITH_MEMPOOL)
endif()

# Implement --use-domain and declare USE_DOMAIN.
#------------------------------------------------------------------------------
option(USE_DOMAIN "Domain enabled." OFF)
if (USE_DOMAIN)
  message(STATUS "Bitprim: Using Domain enabled")
  add_definitions(-DBITPRIM_USE_DOMAIN)
endif()

# Implement and declare DB_TRANSACTION_UNCONFIRMED.
#------------------------------------------------------------------------------
option(DB_TRANSACTION_UNCONFIRMED "DB Transactions Unconfirmed enabled." OFF)
if (DB_TRANSACTION_UNCONFIRMED)
  message(STATUS "Bitprim: DB Transactions Unconfirmed enabled")
  add_definitions(-DBITPRIM_DB_TRANSACTION_UNCONFIRMED)
endif()

# Implement and declare DB_SPENDS.
#------------------------------------------------------------------------------
option(DB_SPENDS "DB Spends enabled." OFF)
if (DB_SPENDS)
  message(STATUS "Bitprim: DB Spends enabled")
  add_definitions(-DBITPRIM_DB_SPENDS)
endif()

# Implement and declare DB_HISTORY.
#------------------------------------------------------------------------------
option(DB_HISTORY "DB History enabled." OFF)
if (DB_HISTORY)
  message(STATUS "Bitprim: DB History enabled")
  add_definitions(-DBITPRIM_DB_HISTORY)
endif()

# Implement and declare DB_STEALTH.
#------------------------------------------------------------------------------
option(DB_STEALTH "DB Stealth enabled." OFF)
if (DB_STEALTH)
  message(STATUS "Bitprim: DB Stealth enabled")
  add_definitions(-DBITPRIM_DB_STEALTH)
endif()

# Implement and declare DB_UNSPENT_LIBBITCOIN.
#------------------------------------------------------------------------------
option(DB_UNSPENT_LIBBITCOIN "DB Unspent Libbitcoin enabled." OFF)
if (DB_UNSPENT_LIBBITCOIN)
  message(STATUS "Bitprim: DB Unspent Libbitcoin enabled")
  add_definitions(-DBITPRIM_DB_UNSPENT_LIBBITCOIN)
endif()

# Implement and declare DB_LEGACY.
#------------------------------------------------------------------------------
option(DB_LEGACY "DB Legacy enabled." OFF)
if (DB_LEGACY)
  message(STATUS "Bitprim: DB Legacy enabled")
  add_definitions(-DBITPRIM_DB_LEGACY)
endif()

# Implement and declare DB_NEW.
#------------------------------------------------------------------------------
option(DB_NEW "DB New enabled." OFF)
if (DB_NEW)
  message(STATUS "Bitprim: DB New enabled")
  add_definitions(-DBITPRIM_DB_NEW)
endif()

# Implement and declare DB_NEW_BLOCKS.
#------------------------------------------------------------------------------
option(DB_NEW_BLOCKS "DB Blocks New enabled." OFF)
if (DB_NEW_BLOCKS)
  message(STATUS "Bitprim: DB Blocks New enabled")
  add_definitions(-DBITPRIM_DB_NEW_BLOCKS)
endif()

# Implement and declare DB_NEW_FULL.
#------------------------------------------------------------------------------
option(DB_NEW_FULL "DB New Full enabled." OFF)
if (DB_NEW_FULL)
  message(STATUS "Bitprim: DB New Full enabled")
  add_definitions(-DBITPRIM_DB_NEW_FULL)
endif()

# Conan infrastructure
#==============================================================================
if(EXISTS ${CMAKE_SOURCE_DIR}/ci_utils/cmake/bitprimbuildinfo.cmake)
    include(${CMAKE_SOURCE_DIR}/ci_utils/cmake/bitprimbuildinfo.cmake)
else()
    message( STATUS "bitprimbuildinfo doent exists")
endif()



# Check dependencies.
#==============================================================================
#------------------------------------------------------------------------------
if (NOT USE_CONAN)
  if (NOT TARGET bitprim-node)
    find_package(bitprim-node 0 REQUIRED)
  endif()

  if (WITH_RPC)
    # Require bitprim-rpc of at least version 0
    #------------------------------------------------------------------------------
    if (NOT TARGET bitprim-rpc)
      find_package(bitprim-rpc 0 REQUIRED)
    endif()
  endif()
endif()


# Set flags.
#==============================================================================
include(CheckCXXCompilerFlag)

# Including common functions
#------------------------------------------------------------------------------
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/ci_utils/cmake)

include(BitprimTools)


# Warn on all stuff.
#------------------------------------------------------------------------------
if (NOT MSVC)
  _add_c_compile_flag(-Wall _has_all_warning_flag)
else()
  _add_c_compile_flag(-W4 _has_all_warning_flag)
  add_definitions(-D_SCL_SECURE_NO_WARNINGS)
  add_definitions(-D_CRT_SECURE_NO_WARNINGS)
endif()

# Warn on extra stuff.
#------------------------------------------------------------------------------
if (NOT MSVC)
  _add_c_compile_flag(-Wextra _has_extra_warning_flag)
endif()

# Be really annoying.
#------------------------------------------------------------------------------
_add_c_compile_flag(-Wpedantic _has_pedantic_warning_flag)
if (_has_pedantic_warning_flag)
  _add_c_compile_flag(-pedantic _has_pedantic_flag)
endif()

# Conform to style.
#------------------------------------------------------------------------------
_add_cxx_compile_flag(-Wno-missing-braces _has_no_missing_braces_warning_flag)

# Conflict in stdlib under clang. Enabled in clang only.
#------------------------------------------------------------------------------
_add_cxx_compile_flag(-Wno-mismatched-tags _has_no_mismatched_tags_warning_flag)

# Clean up boost 1.55 headers. Enabled in gcc only.
#------------------------------------------------------------------------------
_add_c_compile_flag(-Wno-deprecated-declarations _has_no_deprecated_declarations_warning_flag)

# Protect stack.
#------------------------------------------------------------------------------
_add_link_flag(-fstack-protector _has_stack_protector_flag)

# Protect stack comprehensively.
#------------------------------------------------------------------------------
_add_link_flag(-fstack-protector-all _has_stack_protector_all_flag)

# Hide internal functions from external libs. Enabled in gcc only.
#------------------------------------------------------------------------------
_add_cxx_compile_flag(-fvisibility-hidden _has_visibility_hidden_flag)

# Hide inlines from external libs. Enabled in gcc only.
#------------------------------------------------------------------------------
_add_cxx_compile_flag(-fvisibility-inlines-hidden _has_visibility_inlines_hidden_flag)

# Target Windows Vista. Enabled in msvc only.
#------------------------------------------------------------------------------
if (MSVC) # OR MINGW)
  add_definitions(-D_WIN32_WINNT=0x0600)
endif()

# Build
#==============================================================================
add_executable(console.bn
        console/executor.cpp
        console/executor.hpp
        console/main.cpp
        console/user_agent.cpp)

# target_link_libraries(console.bn bitprim-node)


# target_compile_definitions(console.bn PUBLIC -DBITPRIM_BUILD_NUMBER="${BITPRIM_BUILD_NUMBER}")

target_compile_definitions(console.bn PUBLIC -DBITPRIM_PROJECT_VERSION="${BITPRIM_PROJECT_VERSION}") #TODO(fernando): manage with Conan????
target_compile_definitions(console.bn PUBLIC -DBCN_STATIC -DBCB_STATIC -DBCD_STATIC -DBCT_STATIC -DBC_STATIC)

if (NOT USE_CONAN)
  target_link_libraries(console.bn PUBLIC bitprim-node)
  if(WITH_RPC)
    target_link_libraries(console.bn PUBLIC bitprim-rpc)
  endif()
endif()

if (NOT NO_CONAN_AT_ALL)
  target_link_libraries(console.bn PUBLIC ${CONAN_LIBS})
endif()

if (USE_CONAN)
  if (MINGW)
    target_link_libraries(console.bn PUBLIC ws2_32 wsock32) #TODO(fernando): manage with Conan
  endif()
endif()

set_target_properties(
        console.bn PROPERTIES
        FOLDER "node"
        OUTPUT_NAME bn)






# Install
#==============================================================================
install(TARGETS console.bn
        RUNTIME DESTINATION bin)

# # Export
# #==============================================================================
# include(CMakePackageConfigHelpers)

# export(EXPORT bitprim-node
#         FILE "${CMAKE_CURRENT_BINARY_DIR}/bitprim-nodeTargets.cmake")
# export(PACKAGE bitprim-node)

# configure_file(bitprim-nodeConfig.cmake.in
#         "${CMAKE_CURRENT_BINARY_DIR}/bitprim-nodeConfig.cmake"
#         @ONLY)

# write_basic_package_version_file(
#         "${CMAKE_CURRENT_BINARY_DIR}/bitprim-nodeConfigVersion.cmake"
#         VERSION ${PROJECT_VERSION}
#         COMPATIBILITY AnyNewerVersion)

# install(
#         FILES
#         "${CMAKE_CURRENT_BINARY_DIR}/bitprim-nodeConfig.cmake"
#         "${CMAKE_CURRENT_BINARY_DIR}/bitprim-nodeConfigVersion.cmake"
#         DESTINATION ${_config_package_location})
