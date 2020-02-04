# Copyright (c) 2016-2020 Knuth Project developers.
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.


from conans import CMake
from ci_utils import option_on_off, march_conan_manip, pass_march_to_compiler, is_development_branch_internal
from ci_utils import KnuthConanFile

class KnuthNodeExeConan(KnuthConanFile):
    name = "node-exe"
    # version = get_version()
    license = "http://www.boost.org/users/license.html"
    url = "https://github.com/k-nuth/node-exe"
    description = "Bitcoin full node executable"
    settings = "os", "compiler", "build_type", "arch"

    # if Version(conan_version) < Version(get_conan_req_version()):
    #     raise Exception ("Conan version should be greater or equal than %s. Detected: %s." % (get_conan_req_version(), conan_version))

    options = {
        "currency": ['BCH', 'BTC', 'LTC'],
        "with_rpc": [True, False],
        "microarchitecture": "ANY", #["x86_64", "haswell", "ivybridge", "sandybridge", "bulldozer", ...]
        "no_compilation": [True, False],
        "fix_march": [True, False],
        "verbose": [True, False],
        "keoken": [True, False],
        "mempool": [True, False],
        "use_domain": [True, False],
        "db": ['legacy', 'legacy_full', 'pruned', 'default', 'full'],
        "cxxflags": "ANY",
        "cflags": "ANY",
        "glibcxx_supports_cxx11_abi": "ANY",        
    }

    default_options = "currency=BCH", \
                      "with_rpc=False",  \
                      "microarchitecture=_DUMMY_",  \
                      "no_compilation=False",  \
                      "fix_march=False", \
                      "verbose=False", \
                      "keoken=False", \
                      "mempool=False", \
                      "use_domain=True", \
                      "db=default", \
                      "cxxflags=_DUMMY_", \
                      "cflags=_DUMMY_", \
                      "glibcxx_supports_cxx11_abi=_DUMMY_"


    generators = "cmake"
    exports = "conan_*", "ci_utils/*"
    exports_sources = "CMakeLists.txt", "cmake/*", "console/*"

    # package_files = "build/lkth-node.a"
    build_policy = "missing"

    @property
    def is_keoken(self):
        return self.options.currency == "BCH" and self.options.with_rpc and self.options.get_safe("keoken")

    @property
    def dont_compile(self):
        return self.options.no_compilation or (self.settings.compiler == None and self.settings.arch == 'x86_64' and  self.settings.os in ('Linux', 'Windows', 'Macos'))

    def requirements(self):
        if not self.options.no_compilation and self.settings.get_safe("compiler") is not None:
            self.requires("kth-node/0.X@%s/%s" % (self.user, self.channel))

            if self.options.with_rpc:
                self.requires("bitprim-rpc/0.X@%s/%s" % (self.user, self.channel))

    def config_options(self):
        if self.settings.arch != "x86_64":
            self.output.info("microarchitecture is disabled for architectures other than x86_64, your architecture: %s" % (self.settings.arch,))
            self.options.remove("microarchitecture")
            self.options.remove("fix_march")

    def configure(self):
        KnuthConanFile.configure(self)
        # self.output.info("************************************** def configure(self):")

        if self.settings.arch == "x86_64" and self.options.microarchitecture == "_DUMMY_":
            del self.options.fix_march
            # self.options.remove("fix_march")
            # raise Exception ("fix_march option is for using together with microarchitecture option.")

        # if self.options.no_compilation or (self.settings.compiler == None and self.settings.arch == 'x86_64' and self.settings.os in ('Linux', 'Windows', 'Macos')):
        if self.dont_compile:
            self.settings.remove("compiler")
            self.settings.remove("build_type")

        if self.settings.arch == "x86_64":
            march_conan_manip(self)
            self.options["*"].microarchitecture = self.options.microarchitecture

        if self.options.keoken and not self.options.with_rpc:
            self.output.warn("Keoken is only available building with Json-RPC support. Building without Keoken support...")
            del self.options.keoken

        if self.is_keoken and self.options.currency != "BCH":
            self.output.warn("For the moment Keoken is only enabled for BCH. Building without Keoken support...")
            del self.options.keoken


        if self.is_keoken:
            if self.options.db == "pruned" or self.options.db == "default":
                self.output.warn("Keoken mode requires db=full and your configuration is db=%s, it has been changed automatically..." % (self.options.db,))
                self.options.db = "full"


        self.options["*"].db = self.options.db
        
        self.options["*"].keoken = self.is_keoken
        self.options["*"].use_domain = self.options.use_domain

        self.options["*"].mempool = self.options.mempool
        self.output.info("Compiling with mempool: %s" % (self.options.mempool,))

        self.options["*"].currency = self.options.currency
        self.output.info("Compiling for currency: %s" % (self.options.currency,))

        self.options["*"].with_rpc = self.options.with_rpc
        self.output.info("Compiling with RPC support: %s" % (self.options.with_rpc,))

        self.output.info("Compiling for DB: %s" % (self.options.db,))

    def package_id(self):
        KnuthConanFile.package_id(self)
        # self.output.info("************************************** def package_id(self):")

        if self.dont_compile:
            self.info.requires.clear()
            # self.settings.remove("compiler")
            # self.settings.remove("build_type")

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
        self.info.options.verbose = "ANY"
        self.info.options.fix_march = "ANY"
        self.info.options.cxxflags = "ANY"
        self.info.options.cflags = "ANY"


    def deploy(self):
        self.copy("bn.exe", src="bin")     # copy from current package
        self.copy("bn", src="bin")         # copy from current package
        # self.copy_deps("*.dll") # copy from dependencies        

    def build(self):
        cmake = CMake(self)
        cmake.definitions["USE_CONAN"] = option_on_off(True)
        cmake.definitions["NO_CONAN_AT_ALL"] = option_on_off(False)
        cmake.verbose = self.options.verbose
        cmake.definitions["WITH_RPC"] = option_on_off(self.options.with_rpc)
        cmake.definitions["WITH_KEOKEN"] = option_on_off(self.is_keoken)

        cmake.definitions["CURRENCY"] = self.options.currency
        cmake.definitions["WITH_MEMPOOL"] = option_on_off(self.options.mempool)
        cmake.definitions["USE_DOMAIN"] = option_on_off(self.options.use_domain)

        if self.options.db == "legacy":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_NEW"] = option_on_off(False)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "legacy_full":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(True)
            cmake.definitions["DB_SPENDS"] = option_on_off(True)
            cmake.definitions["DB_HISTORY"] = option_on_off(True)
            cmake.definitions["DB_STEALTH"] = option_on_off(True)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_NEW"] = option_on_off(False)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "pruned":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_NEW"] = option_on_off(True)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "default":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_NEW"] = option_on_off(True)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(True)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "full":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_NEW"] = option_on_off(True)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(True)

        if self.settings.compiler != "Visual Studio":
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " -Wno-deprecated-declarations"
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " /DBOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"

        if self.options.cxxflags != "_DUMMY_":
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " " + str(self.options.cxxflags)
        if self.options.cflags != "_DUMMY_":
            cmake.definitions["CONAN_C_FLAGS"] = cmake.definitions.get("CONAN_C_FLAGS", "") + " " + str(self.options.cflags)

        cmake.definitions["MICROARCHITECTURE"] = self.options.microarchitecture
        cmake.definitions["KTH_PROJECT_VERSION"] = self.version

        if self.settings.get_safe("compiler") is not None:
            if self.settings.compiler == "gcc":
                if float(str(self.settings.compiler.version)) >= 5:
                    cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(False)
                else:
                    cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(True)
            elif self.settings.compiler == "clang":
                if str(self.settings.compiler.libcxx) == "libstdc++" or str(self.settings.compiler.libcxx) == "libstdc++11":
                    cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(False)

            pass_march_to_compiler(self, cmake)

        cmake.configure(source_dir=self.source_folder)
        cmake.build()

    # def imports(self):
    #     self.copy("*.h", "", "include")

    def package(self):
        self.copy("bn.exe", dst="bin", src="bin") # Windows
        self.copy("bn", dst="bin", src="bin") # Linux / Macos

    # def package_info(self):
        # self.cpp_info.includedirs = ['include']
        # self.cpp_info.libs = ["kth-node-exe"]







# def option_on_off(option):
#     return "ON" if option else "OFF"

# def get_content(file_name):
#     file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
#     with open(file_path, 'r') as f:
#         return f.read().replace('\n', '').replace('\r', '')

# def get_version():
#     return get_content('conan_version')

# def get_channel():
#     return get_content('conan_channel')

# def get_conan_req_version():
#     return get_content('conan_req_version')

# microarchitecture_default = 'x86_64'

# def get_cpuid():
#     try:
#         # print("*** cpuid OK")
#         cpuid = importlib.import_module('cpuid')
#         return cpuid
#     except ImportError:
#         print("*** cpuid could not be imported")
#         return None

# def get_cpu_microarchitecture_or_default(default):
#     cpuid = get_cpuid()
#     if cpuid != None:
#         # return '%s%s' % cpuid.cpu_microarchitecture()
#         return '%s' % (''.join(cpuid.cpu_microarchitecture()))
#     else:
#         return default

# def get_cpu_microarchitecture():
#     return get_cpu_microarchitecture_or_default(microarchitecture_default)
