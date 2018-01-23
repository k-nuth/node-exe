import platform
from conan.packager import ConanMultiPackager
import os
import cpuid
import copy

if __name__ == "__main__":
    builder = ConanMultiPackager(username="bitprim", channel="testing",
                                 remotes="https://api.bintray.com/conan/bitprim/bitprim",
                                 archs=["x86_64"])

    # builder.add_common_builds(shared_option_name="bitprim-node:shared")
    builder.add_common_builds()

    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["build_type"] == "Release" \
                and (not "compiler.runtime" in settings or not settings["compiler.runtime"] == "MT"):

            env_vars["BITPRIM_BUILD_NUMBER"] = os.getenv('BITPRIM_BUILD_NUMBER', '-')
                
            # opt1 = copy.deepcopy(options)
            # opt2 = copy.deepcopy(options)

            # opt1["bitprim-node-exe:with_rpc"] = "True"
            # opt2["bitprim-node-exe:with_rpc"] = "False"

            # filtered_builds.append([settings, opt1, env_vars, build_requires])
            # filtered_builds.append([settings, opt2, env_vars, build_requires])


            opt1 = copy.deepcopy(options)
            opt2 = copy.deepcopy(options)
            opt3 = copy.deepcopy(options)
            opt4 = copy.deepcopy(options)
            opt5 = copy.deepcopy(options)
            opt6 = copy.deepcopy(options)
            opt7 = copy.deepcopy(options)
            opt8 = copy.deepcopy(options)

            # opt1["bitprim-node-exe:microarchitecture"] = "x86_64"
            # opt1["bitprim-node-exe:with_rpc"] = "True"

            opt2["bitprim-node-exe:microarchitecture"] = "x86_64"
            opt2["bitprim-node-exe:with_rpc"] = "False"
            
            # opt3["bitprim-node-exe:microarchitecture"] = ''.join(cpuid.cpu_microarchitecture())
            # opt3["bitprim-node-exe:with_rpc"] = "True"

            opt4["bitprim-node-exe:microarchitecture"] = ''.join(cpuid.cpu_microarchitecture())
            opt4["bitprim-node-exe:with_rpc"] = "False"

            # opt5["bitprim-node-exe:microarchitecture"] = "haswell"
            # opt5["bitprim-node-exe:with_rpc"] = "True"

            opt6["bitprim-node-exe:microarchitecture"] = "haswell"
            opt6["bitprim-node-exe:with_rpc"] = "False"

            # opt7["bitprim-node-exe:microarchitecture"] = "skylake"
            # opt7["bitprim-node-exe:with_rpc"] = "True"

            opt8["bitprim-node-exe:microarchitecture"] = "skylake"
            opt8["bitprim-node-exe:with_rpc"] = "False"

            # filtered_builds.append([settings, opt1, env_vars, build_requires])
            filtered_builds.append([settings, opt2, env_vars, build_requires])
            # filtered_builds.append([settings, opt3, env_vars, build_requires])
            filtered_builds.append([settings, opt4, env_vars, build_requires])
            # filtered_builds.append([settings, opt5, env_vars, build_requires])
            filtered_builds.append([settings, opt6, env_vars, build_requires])
            # filtered_builds.append([settings, opt7, env_vars, build_requires])
            filtered_builds.append([settings, opt8, env_vars, build_requires])




    builder.builds = filtered_builds
    builder.run()
