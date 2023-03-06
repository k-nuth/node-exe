# Copyright (c) 2016-2023 Knuth Project developers.
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import os
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.errors import ConanInvalidConfiguration
from kthbuild import option_on_off, march_conan_manip, pass_march_to_compiler
from kthbuild import KnuthConanFile

class KnuthNodeExeConan(KnuthConanFile):
    def recipe_dir(self):
        return os.path.dirname(os.path.abspath(__file__))

    name = "kth"
    license = "http://www.boost.org/users/license.html"
    url = "https://github.com/k-nuth/kth"
    description = "Bitcoin full node executable"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "currency": ['BCH', 'BTC', 'LTC'],
        "rpc": [True, False],
        "no_compilation": [True, False],

        "march_id": "ANY",
        "march_strategy": ["download_if_possible", "optimized", "download_or_fail"],

        "verbose": [True, False],
        "mempool": [True, False],
        "db": ['legacy', 'legacy_full', 'pruned', 'default', 'full'],
        "db_readonly": [True, False],

        "cxxflags": "ANY",
        "cflags": "ANY",
        "glibcxx_supports_cxx11_abi": "ANY",
        "cmake_export_compile_commands": [True, False],
        "log": ["boost", "spdlog", "binlog"],
        "use_libmdbx": [True, False],
        "statistics": [True, False],
    }

    default_options = {
        "currency": "BCH",
        "rpc": False,
        "no_compilation": False,

        "march_id": "_DUMMY_",
        "march_strategy": "download_if_possible",

        "verbose": False,
        "mempool": False,
        "db": "default",
        "db_readonly": False,

        "cxxflags": "_DUMMY_",
        "cflags": "_DUMMY_",
        "glibcxx_supports_cxx11_abi": "_DUMMY_",
        "cmake_export_compile_commands": False,
        "log": "spdlog",
        "use_libmdbx": False,
        "statistics": False,
    }

    # generators = "cmake"
    exports = "conan_*", "ci_utils/*"
    exports_sources = "CMakeLists.txt", "cmake/*", "src/*"

    # build_policy = "missing"

    @property
    def dont_compile(self):
        return self.options.no_compilation or (self.settings.compiler == None and self.settings.arch == 'x86_64' and self.settings.os in ('Linux', 'Windows', 'Macos'))

    def requirements(self):
        if not self.options.no_compilation and self.settings.get_safe("compiler") is not None:
            self.requires("node/0.X@%s/%s" % (self.user, self.channel))

            if self.options.rpc:
                self.requires("rpc/0.X@%s/%s" % (self.user, self.channel))

    # def validate(self):
    #     if self.settings.os == "Linux" and self.settings.compiler == "gcc" and self.settings.compiler.libcxx == "libstdc++":
    #         raise ConanInvalidConfiguration("We just support GCC C++11ABI.\n**** Please run `conan profile update settings.compiler.libcxx=libstdc++11 default`")

    def validate(self):
        KnuthConanFile.validate(self)
        if self.info.settings.compiler.cppstd:
            check_min_cppstd(self, "20")

    def config_options(self):
        KnuthConanFile.config_options(self)

    def configure(self):
        KnuthConanFile.configure(self)

        # if self.options.no_compilation or (self.settings.compiler == None and self.settings.arch == 'x86_64' and self.settings.os in ('Linux', 'Windows', 'Macos')):
        if self.dont_compile:
            self.settings.remove("compiler")
            self.settings.remove("build_type")

        self.options["*"].db_readonly = self.options.db_readonly
        self.output.info("Compiling with read-only DB: %s" % (self.options.db_readonly,))

        self.options["*"].mempool = self.options.mempool
        self.output.info("Compiling with mempool: %s" % (self.options.mempool,))

        self.options["*"].rpc = self.options.rpc
        self.output.info("Compiling with RPC support: %s" % (self.options.rpc,))

        #TODO(fernando): move to kthbuild
        self.options["*"].log = self.options.log
        self.output.info("Compiling with log: %s" % (self.options.log,))

        self.options["*"].use_libmdbx = self.options.use_libmdbx
        self.output.info("Compiling with use_libmdbx: %s" % (self.options.use_libmdbx,))

        self.options["*"].statistics = self.options.statistics
        self.output.info("Compiling with statistics: %s" % (self.options.statistics,))

    def package_id(self):
        KnuthConanFile.package_id(self)

        if self.dont_compile:
            self.info.requires.clear()

            self.output.info("package_id - self.channel: %s" % (self.channel,))
            self.output.info("package_id - self.options.no_compilation: %s" % (self.options.no_compilation,))
            self.output.info("package_id - self.settings.compiler: %s" % (self.settings.compiler,))
            self.output.info("package_id - self.settings.arch: %s" % (self.settings.arch,))
            self.output.info("package_id - self.settings.os: %s" % (self.settings.os,))
            self.output.info("package_id - is_development_branch_internal: %s" % (is_development_branch_internal(self.channel),))

            # if not is_development_branch_internal(self.channel):
                # self.info.settings.compiler = "ANY"
                # self.info.settings.build_type = "ANY"
            self.info.settings.compiler = "ANY"
            self.info.settings.build_type = "ANY"

        self.info.options.no_compilation = "ANY"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = self.cmake_toolchain_basis()
        # tc.variables["CMAKE_VERBOSE_MAKEFILE"] = True
        tc.variables["WITH_RPC"] = option_on_off(self.options.rpc)
        tc.variables["WITH_MEMPOOL"] = option_on_off(self.options.mempool)
        tc.variables["DB_READONLY_MODE"] = option_on_off(self.options.db_readonly)
        tc.variables["LOG_LIBRARY"] = self.options.log
        tc.variables["USE_LIBMDBX"] = option_on_off(self.options.use_libmdbx)
        tc.variables["STATISTICS"] = option_on_off(self.options.statistics)
        tc.variables["CONAN_DISABLE_CHECK_COMPILER"] = option_on_off(True)
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        if not self.options.cmake_export_compile_commands:
            cmake.build()
            # if self.options.tests:
            #     cmake.test()

    def package(self):
        self.copy("kth.exe", dst="bin", src="bin")  # Windows
        self.copy("kth", dst="bin", src="bin")      # Unixes

    def deploy(self):
        self.copy("kth.exe", src="bin")     # copy from current package
        self.copy("kth", src="bin")         # copy from current package
        # self.copy_deps("*.dll") # copy from dependencies
