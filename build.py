import copy
import os
import cpuid
import platform
from kthbuild import get_base_march_ids, get_builder, handle_microarchs, copy_env_vars, filter_valid_exts, filter_marchs_tests

if __name__ == "__main__":

    full_build = os.getenv('KTH_FULL_BUILD', '0') == '1'
    builder, name = get_builder(os.path.dirname(os.path.abspath(__file__)))
    builder.add_common_builds(shared_option_name="%s:shared" % name)

    march_ids = get_base_march_ids()
    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:

        if settings["build_type"] == "Release" \
                and (not "compiler.runtime" in settings or not settings["compiler.runtime"] == "MD"):

            copy_env_vars(env_vars)

            ci_currency = os.getenv('KTH_CI_CURRENCY', None)
            if ci_currency is not None:
                options["*:currency"] = ci_currency

                rpc_off = copy.deepcopy(options)
                rpc_on = copy.deepcopy(options)
                rpc_off["*:rpc"] = "False"
                rpc_on["*:rpc"] = "True"

                rpc_off_full = copy.deepcopy(rpc_off)
                rpc_on_full = copy.deepcopy(rpc_on)
                rpc_off_full["*:db"] = "full"
                rpc_on_full["*:db"] = "full"
                
                # if ci_currency == "BCH":
                #     # rpc_on_keoken = copy.deepcopy(rpc_on)
                #     # rpc_on_keoken["*:keoken"] = True
                #     # rpc_on_keoken["*:db"] = "full"

                #     opts_bch_domain = copy.deepcopy(rpc_off)
                #     opts_bch_domain["%s:use_domain" % name] = "True"

                #     handle_microarchs("*:march_id", march_ids, filtered_builds, settings, opts_bch_domain, env_vars, build_requires)
                #     # handle_microarchs("*:march_id", march_ids, filtered_builds, settings, rpc_on_keoken, env_vars, build_requires)
                
                handle_microarchs("*:march_id", march_ids, filtered_builds, settings, rpc_off_full, env_vars, build_requires)
                handle_microarchs("*:march_id", march_ids, filtered_builds, settings, rpc_on_full, env_vars, build_requires)
                handle_microarchs("*:march_id", march_ids, filtered_builds, settings, rpc_on, env_vars, build_requires)
                handle_microarchs("*:march_id", march_ids, filtered_builds, settings, rpc_off, env_vars, build_requires)


    builder.builds = filtered_builds
    builder.run()
