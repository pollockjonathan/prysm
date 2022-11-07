#!/bin/python3
# ModBazel.sh
#
# This file injects the most recent commit to jp/custom_main of:
#   (1) https://github.com/pollockjonathan/go-libp2p
#   (2) https://github.com/pollockjonathan/go-libp2p-pubsub
# Into the deps.bzl file for:
#   (*) https://github.com/pollockjonathan/prysm
#
# This script expects (*)'s root directory to be the $PWD.
# Once injected, the $PWD should be built with the following command:
# $ bazel build //cmd/beacon-chain:beacon-chain --config=release

# Find the relevant go_repository lines. These exist with the following names:
#   (1) com_github_libp2p_go_libp2p
#   (2) com_github_libp2p_go_libp2p_pubsub
#
# This file expects to be called with the assocated commit hash as follows:
# $ ./ModBazel.py ${libp2p_commit_hash} ${libp2p_pubsub_commit_hash}
import sys

with open('./deps.bzl', 'r') as fr:
    lines = fr.readlines()
com_github_libp2p_go_libp2p_index = -1
com_github_libp2p_go_libp2p_pubsub_index = -1
for (ii, line) in enumerate(lines):
    if '\"com_github_libp2p_go_libp2p\"' in line:
        com_github_libp2p_go_libp2p_index = ii
    if '\"com_github_libp2p_go_libp2p_pubsub\"' in line:
        com_github_libp2p_go_libp2p_pubsub_index = ii
print(f'go-libp2p line: {com_github_libp2p_go_libp2p_index}')
print(f'go-libp2p-pubsub line: {com_github_libp2p_go_libp2p_pubsub_index}')

# Find the encapsulating go_repository lines.
com_github_libp2p_go_libp2p_open = com_github_libp2p_go_libp2p_index - 1
com_github_libp2p_go_libp2p_close = com_github_libp2p_go_libp2p_index
while ')' not in lines[com_github_libp2p_go_libp2p_close]:
    com_github_libp2p_go_libp2p_close += 1

com_github_libp2p_go_libp2p_pubsub_open = com_github_libp2p_go_libp2p_pubsub_index - 1
com_github_libp2p_go_libp2p_pubsub_close = com_github_libp2p_go_libp2p_pubsub_index
while ')' not in lines[com_github_libp2p_go_libp2p_pubsub_close]:
    com_github_libp2p_go_libp2p_pubsub_close += 1

# Construct the output arrays.
libp2p_mod = [lines[com_github_libp2p_go_libp2p_open],
        lines[com_github_libp2p_go_libp2p_index],
        lines[com_github_libp2p_go_libp2p_index + 1],
        lines[com_github_libp2p_go_libp2p_index + 2],
        f'        commit = \"{sys.argv[1]}\",\n',
        '        remote = \"git@github.com:pollockjonathan/go-libp2p.git\",\n',
        '        vcs = \"git\",\n',
        lines[com_github_libp2p_go_libp2p_pubsub_close]]
libp2p_pubsub_mod = [lines[com_github_libp2p_go_libp2p_pubsub_open],
        lines[com_github_libp2p_go_libp2p_pubsub_index],
        lines[com_github_libp2p_go_libp2p_pubsub_index + 1],
        lines[com_github_libp2p_go_libp2p_pubsub_index + 2],
        f'        commit = \"{sys.argv[2]}\",\n',
        '        remote = \"git@github.com:pollockjonathan/go-libp2p-pubsub.git\",\n',
        '        vcs = \"git\",\n',
        lines[com_github_libp2p_go_libp2p_pubsub_close]]

# Inject into lines.
output_lines = []
for (ii, line) in enumerate(lines):
    # Inject the relevant content.
    if ii == com_github_libp2p_go_libp2p_open:
        for libline in libp2p_mod:
            output_lines.append(libline)
    if ii == com_github_libp2p_go_libp2p_pubsub_open:
        for libline in libp2p_pubsub_mod:
            output_lines.append(libline)

    # Skip over overwritten content.
    if ii >= com_github_libp2p_go_libp2p_open and ii <= com_github_libp2p_go_libp2p_close:
        continue
    if ii >= com_github_libp2p_go_libp2p_pubsub_open and ii <= com_github_libp2p_go_libp2p_pubsub_close:
        continue

    # Pull old content.
    output_lines.append(line)

# Overwrite existing deps.bzl file.
for line in output_lines: print(line, end='')
with open('./deps.bzl', 'w') as fw:
    fw.writelines(output_lines)
