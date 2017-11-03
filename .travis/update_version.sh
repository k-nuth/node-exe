#!/bin/bash

function replace_versions {
    # echo $1 #project name
    # echo $2 #build number
    while read p; do
        if [[ $p == *"$1:"* ]]; then
            echo "$1: $2" >> ../console/version.hpp.t
        else
            echo $p >> ../console/version.hpp.t
        fi
    done <../console/version.hpp
    mv ../console/version.hpp{.t,}
}  

set -e
set -x

git config --global user.email "ci@bitprim.org"
git config --global user.name "Bitprim CI"

replace_versions "#define BITPRIM_NODE_EXE_VERSION " "#define BITPRIM_NODE_EXE_VERSION $BITPRIM_BUILD_NUMBER"

cat ../console/version.hpp
git add . ../console/version.hpp
# git commit --message "Travis bitprim-node-cint build: $BITPRIM_BUILD_NUMBER, $TRAVIS_BUILD_NUMBER" || true
# git remote add origin-commit https://${GH_TOKEN}@github.com/bitprim/bitprim-py-native.git > /dev/null 2>&1
# git push --quiet --set-upstream origin-commit ${TRAVIS_BRANCH}  || true

# --------------------------------------------------------------------------------------------------------------------
