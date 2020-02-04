import copy
import os
import cpuid
import platform
from kthbuild import get_base_march_ids, get_builder, handle_microarchs, copy_env_vars, filter_valid_exts, filter_marchs_tests

if __name__ == "__main__":

    builder, name = get_builder(os.path.dirname(os.path.abspath(__file__)))
    builder.add_common_builds()

    march_ids = get_base_march_ids()
    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:

        if settings["build_type"] == "Release" \
                and (not "compiler.runtime" in settings or not settings["compiler.runtime"] == "MD"):

            copy_env_vars(env_vars)

            bch = copy.deepcopy(options)
            btc = copy.deepcopy(options)

            bch["*:currency"] = 'BCH'
            btc["*:currency"] = 'BTC'

            # bch_rpc_off = copy.deepcopy(bch)
            bch_rpc_on = copy.deepcopy(bch)
            # bch_rpc_off["*:rpc"] = "False"
            bch_rpc_on["*:rpc"] = "True"

            # btc_rpc_off = copy.deepcopy(btc)
            btc_rpc_on = copy.deepcopy(btc)
            # btc_rpc_off["*:rpc"] = "False"
            btc_rpc_on["*:rpc"] = "True"

            # bch_rpc_off_full = copy.deepcopy(bch_rpc_off)
            bch_rpc_on_full = copy.deepcopy(bch_rpc_on)
            # bch_rpc_off_full["*:db"] = "full"
            bch_rpc_on_full["*:db"] = "full"

            # btc_rpc_off_full = copy.deepcopy(btc_rpc_off)
            btc_rpc_on_full = copy.deepcopy(btc_rpc_on)
            # btc_rpc_off_full["*:db"] = "full"
            btc_rpc_on_full["*:db"] = "full"

            # handle_microarchs("*:march_id", march_ids, filtered_builds, settings, bch_rpc_off_full, env_vars, build_requires)
            handle_microarchs("*:march_id", march_ids, filtered_builds, settings, bch_rpc_on_full, env_vars, build_requires)
            handle_microarchs("*:march_id", march_ids, filtered_builds, settings, bch_rpc_on, env_vars, build_requires)
            # handle_microarchs("*:march_id", march_ids, filtered_builds, settings, bch_rpc_off, env_vars, build_requires)

            # handle_microarchs("*:march_id", march_ids, filtered_builds, settings, btc_rpc_off_full, env_vars, build_requires)
            # handle_microarchs("*:march_id", march_ids, filtered_builds, settings, btc_rpc_on_full, env_vars, build_requires)
            handle_microarchs("*:march_id", march_ids, filtered_builds, settings, btc_rpc_on, env_vars, build_requires)
            # handle_microarchs("*:march_id", march_ids, filtered_builds, settings, btc_rpc_off, env_vars, build_requires)

            # ci_currency = os.getenv('KTH_CI_CURRENCY', None)
            # if ci_currency is not None:
            #     options["*:currency"] = ci_currency

            #     rpc_off = copy.deepcopy(options)
            #     rpc_on = copy.deepcopy(options)
            #     rpc_off["*:rpc"] = "False"
            #     rpc_on["*:rpc"] = "True"

            #     rpc_off_full = copy.deepcopy(rpc_off)
            #     rpc_on_full = copy.deepcopy(rpc_on)
            #     rpc_off_full["*:db"] = "full"
            #     rpc_on_full["*:db"] = "full"
                                
            #     handle_microarchs("*:march_id", march_ids, filtered_builds, settings, rpc_off_full, env_vars, build_requires)
            #     handle_microarchs("*:march_id", march_ids, filtered_builds, settings, rpc_on_full, env_vars, build_requires)
            #     handle_microarchs("*:march_id", march_ids, filtered_builds, settings, rpc_on, env_vars, build_requires)
            #     handle_microarchs("*:march_id", march_ids, filtered_builds, settings, rpc_off, env_vars, build_requires)


    builder.builds = filtered_builds
    builder.run()
