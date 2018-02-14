import platform
from conan.packager import ConanMultiPackager
import os
import cpuid
import copy

def handle_microarchs(opt_name, microarchs, filtered_builds, settings, options, env_vars, build_requires):
    print(microarchs)
    microarchs = list(set(microarchs))
    print(microarchs)

    for ma in microarchs:
        opts_copy = copy.deepcopy(options)
        opts_copy[opt_name] = ma
        filtered_builds.append([settings, opts_copy, env_vars, build_requires])

if __name__ == "__main__":
    builder = ConanMultiPackager(username="bitprim", channel="testing",
                                 remotes="https://api.bintray.com/conan/bitprim/bitprim",
                                 archs=["x86_64"])

    # builder.add_common_builds(shared_option_name="bitprim-node:shared")
    builder.add_common_builds()

    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["build_type"] == "Release" \
                and (not "compiler.runtime" in settings or not settings["compiler.runtime"] == "MD"):

            env_vars["BITPRIM_BUILD_NUMBER"] = os.getenv('BITPRIM_BUILD_NUMBER', '-')


            opts_bch_rpc_on = copy.deepcopy(options)
            opts_btc_rpc_on = copy.deepcopy(options)
            # opts_ltc_rpc_on = copy.deepcopy(options)
            opts_bch_rpc_off = copy.deepcopy(options)
            opts_btc_rpc_off = copy.deepcopy(options)
            # opts_ltc_rpc_off = copy.deepcopy(options)

            opts_bch_rpc_on["bitprim-node-exe:currency"] = "BCH"
            opts_bch_rpc_on["bitprim-node-exe:with_rpc"] = "True"
            opts_btc_rpc_on["bitprim-node-exe:currency"] = "BTC"
            opts_btc_rpc_on["bitprim-node-exe:with_rpc"] = "True"
            # opts_ltc_rpc_on["bitprim-node-exe:currency"] = "LTC"
            # opts_ltc_rpc_on["bitprim-node-exe:with_rpc"] = "True"

            opts_bch_rpc_off["bitprim-node-exe:currency"] = "BCH"
            opts_bch_rpc_off["bitprim-node-exe:with_rpc"] = "False"
            opts_btc_rpc_off["bitprim-node-exe:currency"] = "BTC"
            opts_btc_rpc_off["bitprim-node-exe:with_rpc"] = "False"
            # opts_ltc_rpc_off["bitprim-node-exe:currency"] = "LTC"
            # opts_ltc_rpc_off["bitprim-node-exe:with_rpc"] = "False"

            marchs = ["x86_64", ''.join(cpuid.cpu_microarchitecture()), "haswell", "skylake"]
            handle_microarchs("bitprim-node-exe:microarchitecture", marchs, filtered_builds, settings, opts_bch_rpc_on, env_vars, build_requires)
            handle_microarchs("bitprim-node-exe:microarchitecture", marchs, filtered_builds, settings, opts_btc_rpc_on, env_vars, build_requires)
            # handle_microarchs("bitprim-node-exe:microarchitecture", marchs, filtered_builds, settings, opts_ltc_rpc_on, env_vars, build_requires)
            handle_microarchs("bitprim-node-exe:microarchitecture", marchs, filtered_builds, settings, opts_bch_rpc_off, env_vars, build_requires)
            handle_microarchs("bitprim-node-exe:microarchitecture", marchs, filtered_builds, settings, opts_btc_rpc_off, env_vars, build_requires)
            # handle_microarchs("bitprim-node-exe:microarchitecture", marchs, filtered_builds, settings, opts_ltc_rpc_off, env_vars, build_requires)

    builder.builds = filtered_builds
    builder.run()
