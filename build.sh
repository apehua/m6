#!/bin/sh

git clean -fd
tar -czf pilas_0.81-1.debian.tar.gz pilas-0.81
cd pilas-0.81
dpkg-buildpackage
