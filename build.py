import copy
import os
import cpuid
import platform
from ci_utils import get_builder, handle_microarchs, copy_env_vars, filter_valid_exts

if __name__ == "__main__":

    full_build = os.getenv('BITPRIM_FULL_BUILD', '0') == '1'
    builder, name = get_builder()
    builder.add_common_builds()

    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:

        if settings["build_type"] == "Release" \
                and (not "compiler.runtime" in settings or not settings["compiler.runtime"] == "MD"):

            copy_env_vars(env_vars)

            if full_build:
                # marchs = ["x86_64", ''.join(cpuid.cpu_microarchitecture()), "haswell", "skylake"]
                marchs = filter_valid_exts(str(platform.system()), str(settings["compiler"]), float(str(settings["compiler.version"])), ['x86-64', 'haswell', 'skylake'])
            else:
                marchs = ["x86-64"]

            ci_currency = os.getenv('BITPRIM_CI_CURRENCY', None)
            if ci_currency is not None:
                options["*:currency"] = ci_currency

                rpc_off = copy.deepcopy(options)
                rpc_on = copy.deepcopy(options)
                rpc_off["*:with_rpc"] = "False"
                rpc_on["*:with_rpc"] = "True"

                rpc_off_full = copy.deepcopy(rpc_off)
                rpc_on_full = copy.deepcopy(rpc_on)
                rpc_off_full["*:db"] = "Full"
                rpc_on_full["*:db"] = "Full"
                
                if ci_currency == "BCH":
                    rpc_on_keoken = copy.deepcopy(rpc_on)
                    rpc_on_keoken["*:keoken"] = True
                    rpc_on_keoken["*:db"] = "full"

                    opts_bch_domain = copy.deepcopy(rpc_off)
                    opts_bch_domain["%s:use_domain" % name] = "True"
                    

                    handle_microarchs("*:microarchitecture", marchs, filtered_builds, settings, opts_bch_domain, env_vars, build_requires)
                    handle_microarchs("*:microarchitecture", marchs, filtered_builds, settings, rpc_on_keoken, env_vars, build_requires)

                
                handle_microarchs("*:microarchitecture", marchs, filtered_builds, settings, rpc_off_full, env_vars, build_requires)
                handle_microarchs("*:microarchitecture", marchs, filtered_builds, settings, rpc_on_full, env_vars, build_requires)
                handle_microarchs("*:microarchitecture", marchs, filtered_builds, settings, rpc_on, env_vars, build_requires)
                handle_microarchs("*:microarchitecture", marchs, filtered_builds, settings, rpc_off, env_vars, build_requires)


    builder.builds = filtered_builds
    builder.run()
