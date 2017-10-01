# Ellida

**Yocto integrated automated testing framework for validating result images based on a specification**

Ellida aims to provide automatic testing and validation of Linux distributions
based on a specification. The purpose is to easily evaluate the compliance of a
distribution with a specification. The framework is intended to be used with
Yocto built distributions.

<img src="https://s-media-cache-ak0.pinimg.com/736x/5a/76/dd/5a76dd560d3550f6aba646b2667f0eb6.jpg" width=150>

Main components
1. The Engine - communication manager
2. The Daemon - test runner, available on the tested system
3. The Controller - UI, used by a tester to execute tests and receive results
4. The Manager - tool that keeps the internal representation of the
specifications organised and up to date

<center><img src="res/ellida_arch.png" width=700></center>

The framework is intened to parse a specification, download a test suite
specific to that specification, add Yocto specific configurations required for
adding all dependencies (test suites and test control component), execute the
tests remotely and return the results.

Currently supported specs are AGL and CGL.

Ellida is a diploma project, the thesis contents that go into details about the
architecture can be found at [Theseis](https://github.com/VoltBit/diploma-thesis).

[Icons source](http://www.flaticon.com/packs/vikings)

### Installation and usage instructions

TODO

