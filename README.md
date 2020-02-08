<!-- <a target="_blank" href="http://semver.org">![Version][badge.version]</a> -->
<!-- <a target="_blank" href="https://cirrus-ci.com/github/k-nuth/node-exe">![Build Status][badge.Cirrus]</a> -->

# Knuth <a target="_blank" href="https://github.com/k-nuth/node-exe/releases">![Github Releases][badge.release]</a> <a target="_blank" href="https://travis-ci.org/k-nuth/node-exe">![Build status][badge.Travis]</a> <a target="_blank" href="https://ci.appveyor.com/projects/k-nuth/node-exe">![Build Status][badge.Appveyor]</a> <a target="_blank" href="https://t.me/knuth_cash">![Telegram][badge.telegram]</a> <a target="_blank" href="https://k-nuth.slack.com/">![Slack][badge.slack]</a>

> Multi-Cryptocurrency full-node and development platform

*Knuth* allows you to run a full [Bitcoin](https://bitcoin.org/)/[Bitcoin Cash](https://www.bitcoincash.org/)/[Litecoin](https://litecoin.org/) node,
with all four main features:
  * Wallet
  * Mining
  * Full blockchain
  * Routing

*Knuth* also works as a cryptocurrency development platform with several programmable APIs:
  * C++
  * C
  * C#
  * Python
  * Javascript
  * Rust
  * Golang

... and networking APIs: 
  * insight: Our implementation of the Insight-API
  * JSON-RPC

## Installation Requirements

- 64-bit machine.
- [Conan](https://www.conan.io/) package manager, version 1.1.0 or newer. See [Conan Installation](http://docs.conan.io/en/latest/installation.html#install-with-pip-recommended).

## Installation Procedure

The *Knuth* executables can be installed on Linux, macOS, FreeBSD, Windows and others. These binaries are pre-built for the most usual operating system/compiler combinations and hosted in an online repository. If there are no pre-built binaries for your platform, a build from source will be attempted.

So, for any platform, an installation can be performed in 3 simple steps:

1. Install the Knuth build helper:
```
pip install kthbuild --user --upgrade
```

2. Configure the Conan remote:
```
conan remote add kth https://api.bintray.com/conan/k-nuth/kth
```

3. Install the appropriate executable:

```
# For Bitcoin Cash
conan install kth/0.X@kth/stable -o currency=BCH
# ... or (BCH is the default crypto)
conan install kth/0.X@kth/stable

# For Bitcoin Core
conan install kth/0.X@kth/stable -o currency=BTC

# For Litecoin
conan install kth/0.X@kth/stable -o currency=LTC
```

## Building from source Requirements

In the case we don't have pre-built binaries for your plarform, it is necessary to build from the source code, so you need to add the following requirements to the previous ones:

- C++17 Conforming Compiler.
- [CMake](https://cmake.org/) building tool, version 3.8 or newer.

## Running the node

In order to run the full node you have to initialize the database and then run the node:

1. Run the following to initialize the database:

```./kth -i```

2. finally, run the node:

```./kth```

The above commands use the default configuration hardcoded in the executable. You can use a configuration file to customize the behavior of the node. In the [kth-config](https://github.com/k-nuth/config) repository you can find some example files.

1. Initialize the database using a configuration file:

```./kth -i -c <configuration file path>```

2. Run the node using a configuration file:

```./kth -c <configuration file path>```

## High performance

Knuth is a high performance node, so our build system has the ability to automatically detect the microarchitecture of your processor and perform an optimized build for it.

For those who don't want to wait for compilation times, we provide a pre-built packages for the instruction set and extensions corresponding to [Intel Haswell](https://en.wikipedia.org/wiki/Haswell_(microarchitecture)).


## Documentation

In you want to tune the installation for better performance, please refer to the [documentation](https://k-nuth.github.io/docs/content/user_guide/advanced_installation.html).

## Changelog

* [0.1.0](https://github.com/k-nuth/kth/blob/master/doc/release-notes/release-notes.md#version-010)

<!-- Links -->
[badge.Travis]: https://travis-ci.org/k-nuth/node-exe.svg?branch=master
[badge.Appveyor]: https://ci.appveyor.com/api/projects/status/github/k-nuth/node-exe?svg=true&branch=master
[badge.Cirrus]: https://api.cirrus-ci.com/github/k-nuth/node-exe.svg?branch=master
[badge.version]: https://badge.fury.io/gh/k-nuth%2Fnode-exe.svg
[badge.release]: https://img.shields.io/github/release/k-nuth/node-exe.svg

[badge.telegram]: https://img.shields.io/badge/telegram-badge-blue.svg?logo=telegram
[badge.slack]: https://img.shields.io/badge/slack-badge-orange.svg?logo=slack

<!-- [badge.Gitter]: https://img.shields.io/badge/gitter-join%20chat-blue.svg -->
