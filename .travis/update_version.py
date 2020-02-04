import sys
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


def replace_version(source_file, search, replace):

    fh, abs_path = mkstemp()

    with fdopen(fh, "w") as new_file:
        with open(source_file) as old_file:
            lines = old_file.read().split("\n")

            for line in lines:
                if line.startswith(search):
                    new_file.write(replace)
                else:
                    new_file.write(line)
                new_file.write('\n')

    remove(source_file)
    move(abs_path, source_file)    


if __name__ == "__main__":

    # print 'Number of arguments:', len(sys.argv), 'arguments.'
    # print 'Argument List:', str(sys.argv)
    # print sys.argv[1:]

    args = sys.argv[1:]
    print(args)

    # print 'args[0]:', args[0]
    # print 'args[1]:', args[1]
    # print 'args[2]:', args[2]

    replace_version(args[0], args[1], args[2])


# set -e
# set -x

# git config --global user.email "ci@kth.cash"
# git config --global user.name "Knuth CI"

# replace_versions "#define KTH_NODE_EXE_VERSION " "#define KTH_NODE_EXE_VERSION $KTH_BUILD_NUMBER"

# cat console/version.hpp
# # git add . console/version.hpp
# # git commit --message "Travis kth-node-cint build: $KTH_BUILD_NUMBER, $TRAVIS_BUILD_NUMBER" || true
# # git remote add origin-commit https://${GH_TOKEN}@github.com/k-nuth/py-native.git > /dev/null 2>&1
# # git push --quiet --set-upstream origin-commit ${TRAVIS_BRANCH}  || true

# # --------------------------------------------------------------------------------------------------------------------
