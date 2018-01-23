#
# Copyright (c) 2017 Bitprim developers (see AUTHORS)
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

import os
from conans import ConanFile, CMake

# import cpuid
cpuid_installed = False
import importlib
try:
    cpuid = importlib.import_module('cpuid')
    cpuid_installed = True
except ImportError:
    # print("*** cpuid could not be imported")
    cpuid_installed = False


def option_on_off(option):
    return "ON" if option else "OFF"

def make_default_options_method():
    defs = ("with_litecoin=False","with_rpc=False",)

    march_opt = ""
    if cpuid_installed:
        march_opt = "microarchitecture=%s" % (''.join(cpuid.cpu_microarchitecture()))
    else:
        march_opt = "microarchitecture=x86_64"

    new_defs = defs + (march_opt,)
    return new_defs


class BitprimNodeExeConan(ConanFile):
    name = "bitprim-node-exe"
    version = "0.7"
    license = "http://www.boost.org/users/license.html"
    url = "https://github.com/bitprim/bitprim-node-exe"
    description = "Bitcoin full node executable"

    # settings = "os", "compiler", "build_type", "arch"
    settings = "os", "arch"

    options = {
        "with_litecoin": [True, False],
        "with_rpc": [True, False],
        "microarchitecture": "ANY" #["x86_64", "haswell", "ivybridge", "sandybridge", "bulldozer", ...]
    }
    
    # default_options = "with_litecoin=False", \
    #     "microarchitecture=x86_64"

    default_options = make_default_options_method()

    generators = "cmake"
    exports_sources = "CMakeLists.txt", "cmake/*", "console/*"
    # package_files = "build/lbitprim-node.a"
    build_policy = "missing"

    # requires = (("bitprim-node/0.7@bitprim/testing"))

    def requirements(self):
        print('def requirements(self):')

        if self.settings.get_safe("compiler") is not None:
            print('compiler exists')
            print(self.settings.compiler)
        else:
            print('compiler removed')
            

        if self.settings.get_safe("compiler") is not None:
            self.requires("bitprim-node/0.7@bitprim/testing")
            if self.options.with_rpc:
                self.requires("bitprim-rpc/0.7@bitprim/testing")

    # def configure(self):
    #     print('def configure(self):')

    #     print(self.settings.os)
    #     print(self.settings.arch)

    #     if self.settings.compiler != None:
    #         print(self.settings.compiler)
    #     else:
    #         print('compiler None')

    #     if self.settings.compiler == None:
    #         if self.settings.arch == 'x86_64':
    #             if self.settings.os in ('Linux', 'Windows', 'Macos'):
    #                 self.settings.remove("compiler")
    #                 self.settings.remove("build_type")
    #                 # del self.settings.compiler
    #                 # del self.settings.build_type


    #         # # If header only, the compiler, etc, does not affect the package!
    #         # if self.options.header_only:
    #         #     self.settings.clear()
    #         #     self.options.remove("static")

    # def package_id(self):
    #     print('def configure(self):')
    #     # self.settings.remove("compiler")
    #     # self.settings.remove("build_type")
    #     self.info.settings.compiler = "ANY"
    #     self.info.settings.build_type = "ANY"


    def build(self):
        cmake = CMake(self)
        
        cmake.definitions["USE_CONAN"] = "ON"
        cmake.definitions["NO_CONAN_AT_ALL"] = "OFF"
        cmake.definitions["CMAKE_VERBOSE_MAKEFILE"] = "OFF"
        cmake.definitions["WITH_LITECOIN"] = option_on_off(self.options.with_litecoin)
        cmake.definitions["WITH_RPC"] = option_on_off(self.options.with_rpc)

        if self.settings.compiler == "gcc":
            if float(str(self.settings.compiler.version)) >= 5:
                cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(False)
            else:
                cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(True)

        cmake.definitions["BITPRIM_BUILD_NUMBER"] = os.getenv('BITPRIM_BUILD_NUMBER', '-')
        cmake.configure(source_dir=self.source_folder)
        cmake.build()

    # def imports(self):
    #     self.copy("*.h", "", "include")

    def package(self):
        # self.copy("*.h", dst="include", src="include")
        # self.copy("*.hpp", dst="include", src="include")
        # self.copy("*.ipp", dst="include", src="include")

        self.copy("bn.exe", dst="bin", src="bin") # Windows
        self.copy("bn", dst="bin", src="bin") # Linux / Macos

        # self.copy("*.lib", dst="lib", keep_path=False)
        # self.copy("*.dll", dst="bin", keep_path=False)
        # self.copy("*.dylib*", dst="lib", keep_path=False)
        # self.copy("*.so", dst="lib", keep_path=False)
        # self.copy("*.a", dst="lib", keep_path=False)


    # def package_info(self):
        # self.cpp_info.includedirs = ['include']
        # self.cpp_info.libs = ["bitprim-node-exe"]
