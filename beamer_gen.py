#!/usr/bin/env python3
import sys
import re


def process_file(filename_in, filename_out):
    """Actual processing of a file."""
    # regular expressions for various directives
    frame_re = re.compile(r'^(\s*)\+ (.*)$')
    section_re = re.compile(r'^s (.*)$')
    block_re = re.compile(r'^(\s*)b (.*)$')
    item_re = re.compile(r'^(\s*)- (.*)$')
    column_re = re.compile(r'^(\s*)c\{(\d*.?\d*)\}$')
    figure_re = re.compile(r'^(\s*)f\{(\d*.?\d*)\}\{(.*)\}$')

    # TODO store actual indentation levels
    def indent():
        """Return current indentation prefix."""
        # FIXME doesn't work well in case of mixed environments
        return '    ' * len(current_envs)

    def close_envs(n=None):
        """Close currently opened environments."""
        if n is None:
            n = len(current_envs)
        assert 0 <= n <= len(current_envs)
        for _ in range(n):
            env_name = current_envs.pop()
            lines.append(indent() + '\\end{{{}}}\n'.format(env_name))

    lines = []
    current_envs = []
    for line in open(filename_in):
        if frame_re.match(line):  # new frame
            frame = frame_re.match(line)
            close_envs()  # frame is always top-level environment
            lines.append(frame.group(1) + '\\begin{frame}\n')
            current_envs.append('frame')
            lines.append(frame.group(1) + '    \\frametitle{{{}}}\n'.format(
                frame.group(2)))
        elif section_re.match(line):  # new section
            section = section_re.match(line)
            close_envs()
            lines.append('\\section{{{}}}\n'.format(section.group(1)))
        else:  # default: passthrough
            lines.append(line)
    # close all remaining environments
    close_envs()
    # TODO reorder all closing environments and empty lines
    with open(filename_out, 'w') as f_out:
        f_out.writelines(lines)


def main():
    """Command line parsing."""
    # TODO real argument parsing
    for filename_in in sys.argv[1:]:
        process_file(filename_in, filename_in+'.tex')

if __name__ == '__main__':
    main()
