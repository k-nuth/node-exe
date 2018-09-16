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
import importlib


def option_on_off(option):
    return "ON" if option else "OFF"

def get_content(file_name):
    # print(os.path.dirname(os.path.abspath(__file__)))
    # print(os.getcwd())
    # print(file_name)
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, 'r') as f:
        return f.read()

def get_version():
    return get_content('conan_version')

def get_channel():
    return get_content('conan_channel')


microarchitecture_default = 'x86_64'

def get_cpuid():
    try:
        # print("*** cpuid OK")
        cpuid = importlib.import_module('cpuid')
        return cpuid
    except ImportError:
        print("*** cpuid could not be imported")
        return None

def get_cpu_microarchitecture_or_default(default):
    cpuid = get_cpuid()
    if cpuid != None:
        # return '%s%s' % cpuid.cpu_microarchitecture()
        return '%s' % (''.join(cpuid.cpu_microarchitecture()))
    else:
        return default

def get_cpu_microarchitecture():
    return get_cpu_microarchitecture_or_default(microarchitecture_default)


    # TODO: check previous marchs
    # TODO: AMD
    # TODO: Intel Linea ATOM
    # TODO: Cyrix y otros procesadores no 80x86

    # Intel Linea "Pulenta". La otra linea es la de ATOM, etc...
    # Nehalem
        # Instructions	
        #     MMX
        # Extensions	
        #     x86-64, Intel 64
        #     SSE, SSE2, SSE3, SSSE3, SSE4, SSE4.1, SSE4.2
        #     VT-x, VT-d

    # Westmere
    #     Instructions	
    #         MMX, AES-NI, CLMUL
    #     Extensions	
    #         x86-64, Intel 64
    #         SSE, SSE2, SSE3, SSSE3, SSE4, SSE4.1, SSE4.2
    #         VT-x, VT-d

    # Sandy Bridge
    #     Instructions	
    #         MMX, AES-NI, CLMUL
    #     Extensions	
    #         x86-64, Intel 64
    #         SSE, SSE2, SSE3, SSSE3, SSE4, SSE4.1, SSE4.2
    #         AVX, TXT, VT-x, VT-d

    # Ivy Bridge
    #     Instructions	
    #         MMX, AES-NI, CLMUL
    #     Extensions	
    #         x86-64, Intel 64
    #         SSE, SSE2, SSE3, SSSE3, SSE4, SSE4.1, SSE4.2
    #         AVX, TXT, VT-x, VT-d, F16C

    # Haswell
    #     Instructions	
    #         MMX, AES-NI, CLMUL, FMA3
    #     Extensions	
    #         x86-64, Intel 64
    #         SSE, SSE2, SSE3, SSSE3, SSE4, SSE4.1, SSE4.2
    #         AVX, AVX2, TXT, and TSX (disabled via microcode, except for Haswell-EX)
    #         VT-x, VT-d    

    # Broadwell
    #     Instructions	
    #         MMX, AES-NI, CLMUL, FMA3
    #     Extensions	
    #         x86-64
    #         SSE, SSE2, SSE3, SSSE3, SSE4, SSE4.1, SSE4.2
    #         AVX, AVX2, TXT, TSX
    #         VT-x, VT-d

    # Skylake
    #     Instructions	
    #         MMX, AES-NI, CLMUL, FMA3
    #     Extensions	
    #         x86-64, Intel 64
    #         SSE, SSE2, SSE3, SSSE3, SSE4, SSE4.1, SSE4.2
    #         ADX, AVX, AVX2, AVX-512 (Xeon 'Purley' only[2][3][4]), MPX, TXT, TSX, SGX[5]
    #         VT-x, VT-d

march_is = [
    {'march': 'nehalem',     'arch': '80x68', 'brand': 'intel', 'iss': ['MMX', 'x86-64', 'Intel 64', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'VT-x', 'VT-d']},
    {'march': 'westmere',    'arch': '80x68', 'brand': 'intel', 'iss': ['MMX', 'AES-NI', 'CLMUL', 'x86-64', 'Intel 64', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'VT-x', 'VT-d']},
    {'march': 'sandybridge', 'arch': '80x68', 'brand': 'intel', 'iss': ['MMX', 'AES-NI', 'CLMUL', 'x86-64', 'Intel 64', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'AVX', 'TXT', 'VT-x', 'VT-d']},
    {'march': 'ivybridge',   'arch': '80x68', 'brand': 'intel', 'iss': ['MMX', 'AES-NI', 'CLMUL', 'x86-64', 'Intel 64', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'AVX', 'TXT', 'VT-x', 'VT-d', 'F16C']},
    # TSX disabled via microcode, except for Haswell-EX
    {'march': 'haswell',     'arch': '80x68', 'brand': 'intel', 'iss': ['MMX', 'AES-NI', 'CLMUL', 'FMA3', 'x86-64', 'Intel 64', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'AVX', 'AVX2', 'TXT', 'VT-x', 'VT-d']},
    {'march': 'haswell-EX',  'arch': '80x68', 'brand': 'intel', 'iss': ['MMX', 'AES-NI', 'CLMUL', 'FMA3', 'x86-64', 'Intel 64', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'AVX', 'AVX2', 'TXT', 'TSX', 'VT-x', 'VT-d']},
    {'march': 'broadwell',   'arch': '80x68', 'brand': 'intel', 'iss': ['MMX', 'AES-NI', 'CLMUL', 'FMA3', 'x86-64', 'Intel 64', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'AVX', 'AVX2', 'TXT', 'TSX', 'VT-x', 'VT-d']},
    {'march': 'skylake',     'arch': '80x68', 'brand': 'intel', 'iss': ['MMX', 'AES-NI', 'CLMUL', 'FMA3', 'x86-64', 'Intel 64', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'ADX', 'AVX', 'AVX2', 'MPX', 'TXT', 'TSX', 'VT-x', 'VT-d']},
        # 'SGX[5]'
        # 'AVX-512 (Xeon 'Purley' only[2][3][4])'

]

 

def transform_is(is_name):
    is_name = is_name.replace(' ', '_')
    is_name = is_name.replace('-', '_')
    is_name = is_name.replace('.', '_')
    return "BITPRIM_HAS_%s" % (is_name.upper(),)

def get_iss(march):
    filtered = (x for x in march_is if x['march'] == march)
    x = next(filtered, None)

    if x != None:
        # print(x)
        # return []
        return x['iss']
    else:
        return []


def add_iss_defs(march, cmake):

    print(march)

    for x in get_iss(march):
        definition = transform_is(x)
        print(x)
        print(definition)
        cmake.definitions[definition] = option_on_off(True)


class BitprimNodeExeConan(ConanFile):
    name = "bitprim-node-exe"

    # version = "0.7"
    version = get_version()

    license = "http://www.boost.org/users/license.html"
    url = "https://github.com/bitprim/bitprim-node-exe"
    description = "Bitcoin full node executable"

    settings = "os", "compiler", "build_type", "arch"
    # settings = "os", "arch"

    options = {
        "currency": ['BCH', 'BTC', 'LTC'],
        "with_rpc": [True, False],
        "microarchitecture": "ANY", #["x86_64", "haswell", "ivybridge", "sandybridge", "bulldozer", ...]
        "no_compilation": [True, False],
        "verbose": [True, False],
    }

    # "with_litecoin": [True, False],
    
    default_options = "currency=BCH", \
                      "with_rpc=False",  \
                      "microarchitecture=_DUMMY_",  \
                      "no_compilation=False",  \
                      "verbose=False"
    
    # "with_litecoin=False",  \

    generators = "cmake"

    exports = "conan_channel", "conan_version"
    exports_sources = "CMakeLists.txt", "cmake/*", "console/*", "bitprimbuildinfo.cmake"

    # package_files = "build/lbitprim-node.a"
    build_policy = "missing"

    def requirements(self):
        # self.output.info('def requirements(self):')

        # if self.settings.get_safe("compiler") is not None:
        #     self.output.info('compiler exists')
        #     self.output.info(self.settings.compiler)
        # else:
        #     self.output.info('compiler removed')

        if not self.options.no_compilation and self.settings.get_safe("compiler") is not None:
            self.requires("bitprim-node/0.8@bitprim/%s" % get_channel())
            if self.options.with_rpc:
                self.requires("bitprim-rpc/0.8@bitprim/%s" % get_channel())


    def configure(self):
        # self.output.info('def configure(self):')

        # self.output.info(self.settings.os)
        # self.output.info(self.settings.arch)

        # if self.settings.compiler != None:
        #     self.output.info(self.settings.compiler)
        # else:
        #     self.output.info('compiler None')

        if self.options.no_compilation or (self.settings.compiler == None and self.settings.arch == 'x86_64' and self.settings.os in ('Linux', 'Windows', 'Macos')):
            self.settings.remove("compiler")
            self.settings.remove("build_type")
            # del self.settings.compiler
            # del self.settings.build_type


            # # If header only, the compiler, etc, does not affect the package!
            # if self.options.header_only:
            #     self.settings.clear()
            #     self.options.remove("static")

        if self.options.microarchitecture == "_DUMMY_":
            self.options.microarchitecture = get_cpu_microarchitecture()

            if get_cpuid() == None:
                march_from = 'default'
            else:
                march_from = 'taken from cpuid'

        else:
            march_from = 'user defined'
        
        self.options["*"].microarchitecture = self.options.microarchitecture
        self.output.info("Compiling for microarchitecture (%s): %s" % (march_from, self.options.microarchitecture))

        self.options["*"].currency = self.options.currency
        self.output.info("Compiling for currency: %s" % (self.options.currency,))

        self.options["*"].with_rpc = self.options.with_rpc
        self.output.info("Compiling with RPC support: %s" % (self.options.with_rpc,))

    def package_id(self):
        self.info.requires.clear()
        # self.settings.remove("compiler")
        # self.settings.remove("build_type")
        self.info.settings.compiler = "ANY"
        self.info.settings.build_type = "ANY"
        self.info.options.no_compilation = "ANY"
        self.info.options.verbose = "ANY"

        

        # self.output.info('def package_id(self):')

        # self.output.info(self.info.requires)
        # self.output.info(self.info.requires.sha)
        # self.output.info(self.info.requires.serialize)
        # self.output.info(self.info.requires.pkg_names)

        # # self.output.info(self.info.requires['bitprim-node/0.8@bitprim/%s' % get_channel())])
        # # self.output.info(self.info.requires['bitprim-node'])

        # # self.info.requires.remove('bitprim-node')
        # # self.info.requires.remove('bitprim-rpc')

        # self.output.info(self.info.requires)
        # self.output.info(self.info.requires.sha)
        # self.output.info(self.info.requires.serialize)
        # self.output.info(self.info.requires.pkg_names)

        # # for x in self.info.requires:
        # #     self.output.info(x)


        # # if self.settings.get_safe("compiler") is not None:
        # #     self.requires("bitprim-node/0.8@bitprim/%s" % get_channel()))
        # #     if self.options.with_rpc:
        # #         self.requires("bitprim-rpc/0.8@bitprim/%s" % get_channel()))

        # self.output.info(self.info.options)
        # self.output.info(self.info.options.sha)
        # self.output.info(self.info.package_id())
        

    def deploy(self):
        self.copy("bn.exe", src="bin")     # copy from current package
        self.copy("bn", src="bin")         # copy from current package
        # self.copy_deps("*.dll") # copy from dependencies        


    def build(self):
        cmake = CMake(self)
        
        cmake.definitions["USE_CONAN"] = option_on_off(True)
        cmake.definitions["NO_CONAN_AT_ALL"] = option_on_off(False)

        # cmake.definitions["CMAKE_VERBOSE_MAKEFILE"] = "OFF"
        # cmake.verbose = False
        cmake.verbose = self.options.verbose
        
        # cmake.definitions["WITH_LITECOIN"] = option_on_off(self.options.with_litecoin)
        cmake.definitions["WITH_RPC"] = option_on_off(self.options.with_rpc)

        cmake.definitions["CURRENCY"] = self.options.currency
        cmake.definitions["MICROARCHITECTURE"] = self.options.microarchitecture

        if self.settings.compiler == "gcc":
            if float(str(self.settings.compiler.version)) >= 5:
                cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(False)
            else:
                cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(True)
        elif self.settings.compiler == "clang":
            if str(self.settings.compiler.libcxx) == "libstdc++" or str(self.settings.compiler.libcxx) == "libstdc++11":
                cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(False)

        cmake.definitions["BITPRIM_BUILD_NUMBER"] = os.getenv('BITPRIM_BUILD_NUMBER', '-')

        add_iss_defs(self.options.microarchitecture, cmake)

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
