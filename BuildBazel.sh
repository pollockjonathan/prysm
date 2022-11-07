#!/bin/bash
# BuildBazel.sh
# 6 November 2022
#
# This script does the following:
#   (1) Finds the most recent commits to jp/main from:
#     (a) https://github.com/pollockjonathan/go-libp2p-pubsub
#     (b) https://github.com/pollockjonathan/go-libp2p
#   (2) Injects them into deps.bzl using ./ModBazel.py
#   (3) Builds Prysm via Bazel
#     (a) bazel build //cmd/beacon-chain:beacon-chain --config=release
#
# NOTE: Ensure both the local and remote jp/main branches are in sync!

# Read in most recent commit hash
IFS=' '; read -a blks <<< $(git -C ../go-libp2p-pubsub log origin/jp/main | head -1)
pubsubHash=${blks[1]}
echo "go-libp2p-pubsub build hash" $pubsubHash
IFS=' '; read -a blks <<< $(git -C ../go-libp2p log origin/jp/main | head -1)
libp2pHash=${blks[1]}
echo "go-libp2p build hash" $libp2pHash

# Inject into deps.bzl
./ModBazel.py $libp2pHash $pubsubHash

# Build the project
bazel build //cmd/beacon-chain:beacon-chain --config=release
