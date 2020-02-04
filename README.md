# Knuth <a target="_blank" href="http://semver.org">![Version][badge.version]</a> <a target="_blank" href="https://travis-ci.org/k-nuth/node-exe">![Travis status][badge.Travis]</a> [![Appveyor Status](https://ci.appveyor.com/api/projects/status/github/k-nuth/node-exe?svg=true&branch=master)](https://ci.appveyor.com/projects/k-nuth/node-exe) <a target="_blank" href="https://gitter.im/kth/Lobby">![Gitter Chat][badge.Gitter]</a>

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

So, for any platform, an installation can be performed in 2 simple steps:

1. Configure the Conan remote
```
conan remote add kth https://api.bintray.com/conan/k-nuth/kth
```

2. Install the appropriate executable

```
# For Bitcoin Cash
conan install kth-node-exe/0.10.1@kth/stable -o currency=BCH
# ... or (BCH is the default crypto)
conan install kth-node-exe/0.10.1@kth/stable

# For Bitcoin Legacy
conan install kth-node-exe/0.10.1@kth/stable -o currency=BTC

# For Litecoin
conan install kth-node-exe/0.10.1@kth/stable -o currency=LTC
```

## Building from source Requirements

In the case we don't have pre-built binaries for your plarform, it is necessary to build from the source code, so you need to add the following requirements to the previous ones:

- C++11 Conforming Compiler.
- [CMake](https://cmake.org/) building tool, version 3.4 or newer.

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

## Advanced Installation

Knuth is a high performance node, so we have some options and pre-built packages tuned for several platforms.
Specifically, you can choose your computer _microarchitecture_ to download a pre-build executable compiled to take advantage of the instructions available in your processor. For example:

```
# For Haswell microarchitecture and Bitcoin Cash currency
conan install kth-node-exe/0.10.1@kth/stable -o currency=BCH -o microarchitecture=haswell 
```
So, you can manually choose the appropriate microarchitecture, some examples are: _x86_64_, _haswell_, _ivybridge_, _sandybridge_, _bulldozer_, ...  
By default, if you do not specify any, the building system will select a base microarchitecture corresponding to your _Instruction Set Architecture_ (ISA). For example, for _Intel 80x86_, the x86_64 microarchitecture will be selected.

### Automatic Microarchitecture selection

Our build system has the ability to automatically detect the microarchitecture of your processor. To do this, first, you have to install our _pip_ package called [cpuid](https://pypi.python.org/pypi/cpuid). Our build system detects if this package is installed and in such case, makes use of it to detect the best possible executable for your processor.

```
pip install cpuid
conan install kth-node-exe/0.10.1@kth/stable
```

## Detailed documentation

* [Gitbook site](https://www.kth.cash/)
* [Build manually from source](https://www.kth.cash/installation.html)
* [Python API documentation](https://www.kth.cash/python-interface/details.html)

## Changelog

* [0.10.0](https://github.com/k-nuth/kth/blob/master/doc/release-notes/release-notes.md#version-0100)
* [0.9.1](https://github.com/k-nuth/kth/blob/master/doc/release-notes/release-notes.md#version-091)
* [0.9](https://github.com/k-nuth/kth/blob/master/doc/release-notes/release-notes.md#version-090)
* [0.8](https://github.com/k-nuth/kth/blob/master/doc/release-notes/release-notes.md#version-080)
* [0.7](https://github.com/k-nuth/kth/blob/master/doc/release-notes/release-notes.md#version-070)
* [Older](https://github.com/k-nuth/kth/blob/master/doc/release-notes/release-notes.md)


<!-- Links -->
[badge.Appveyor]: https://ci.appveyor.com/api/projects/status/github/k-nuth/node-exe?svg=true&branch=dev
[badge.Gitter]: https://img.shields.io/badge/gitter-join%20chat-blue.svg
[badge.Travis]: https://travis-ci.org/k-nuth/node-exe.svg?branch=master
[badge.version]: https://badge.fury.io/gh/kth%2Fkth-node-exe.svg
