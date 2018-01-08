cmake_minimum_required(VERSION 3.4)

# bitprim-node-exe
#==============================================================================
project(bitprim-node-exe
        VERSION 0.5.0
        LANGUAGES CXX C)

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  if (NOT NOT_USE_CPP11_ABI)
    add_definitions(-D_GLIBCXX_USE_CXX11_ABI=1)
  else()
    add_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)
  endif()
  set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -Wno-macro-redefined")
endif()

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Check for baseline language coverage in the compiler for the C++11 standard.
#------------------------------------------------------------------------------
set(CMAKE_CXX_STANDARD 11)
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

# Implement --with-litecoin.
#------------------------------------------------------------------------------
option(WITH_LITECOIN "Compile with Litecoin support." OFF)


set(BITPRIM_BUILD_NUMBER "-" CACHE STRING "Specify the Bitprim Build Number.")


# Conan infrastructure.
#==============================================================================
# Only if enabled
#------------------------------------------------------------------------------
if (NOT NO_CONAN_AT_ALL)
  if(EXISTS ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
      include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
      conan_basic_setup()
  else()
      message(WARNING "The file conanbuildinfo.cmake doesn't exist, you have to run conan install first")
  endif()
endif()

# Check dependencies.
#==============================================================================
#------------------------------------------------------------------------------
if (NOT USE_CONAN)
  if (NOT TARGET bitprim-node)
    find_package(bitprim-node 3.0.0 REQUIRED)
  endif()

  if (WITH_RPC)
    # Require bitprim-rpc of at least version 3.0.0
    #------------------------------------------------------------------------------
    if (NOT TARGET bitprim-rpc)
      find_package(bitprim-rpc 3.0.0 REQUIRED)
    endif()
  endif()

endif()

if (WITH_LITECOIN)
  add_definitions(-DLITECOIN)
endif()

# Set flags.
#==============================================================================
include(CheckCXXCompilerFlag)

# Including common functions
#------------------------------------------------------------------------------
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
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
if (MSVC)
  add_definitions(-D_WIN32_WINNT=0x0600)
endif()


# Build
#==============================================================================
add_executable(console.bn
        console/executor.cpp
        console/executor.hpp
        console/main.cpp)

# target_link_libraries(console.bn bitprim-node)

# target_compile_definitions(console.bn PUBLIC -DBITPRIM_BUILD_NUMBER="\\"${BITPRIM_BUILD_NUMBER}\\"")
target_compile_definitions(console.bn PUBLIC -DBITPRIM_BUILD_NUMBER="${BITPRIM_BUILD_NUMBER}")
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
