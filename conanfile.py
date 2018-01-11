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

    gmp_opt = ""
    if cpuid_installed:
        gmp_opt = "microarchitecture=%s" % (''.join(cpuid.cpu_microarchitecture()))
    else:
        gmp_opt = "microarchitecture=x86_64"

    new_defs = defs + (gmp_opt,)
    return new_defs


class BitprimNodeExeConan(ConanFile):
    name = "bitprim-node-exe"
    version = "0.5"
    license = "http://www.boost.org/users/license.html"
    url = "https://github.com/bitprim/bitprim-node-exe"
    description = "Bitcoin full node executable"
    
    settings = "os", "compiler", "build_type", "arch"

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

    requires = (("bitprim-node/0.5@bitprim/stable"),
                ("bitprim-rpc/0.5@bitprim/stable"))

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
