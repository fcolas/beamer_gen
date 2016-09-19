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

    def indent():
        """Return current indentation prefix."""
        try:
            return '    ' + ' ' * current_envs[-1][1]
        except IndexError:
            return ''

    def close_envs(n=0):
        """Close currently opened environments."""
        while current_envs:
            if n <= current_envs[-1][1]:
                env = current_envs.pop()
                lines.append(indent() + '\\end{{{}}}\n'.format(env[0]))
            else:
                break

    lines = []
    current_envs = []
    for line in open(filename_in):
        if frame_re.match(line):  # new frame
            frame = frame_re.match(line)
            close_envs()  # frame is always top-level environment
            lines.append(frame.group(1) + '\\begin{frame}\n')
            current_envs.append(('frame', len(frame.group(1))))
            lines.append(indent() + '\\frametitle{{{}}}\n'.format(
                frame.group(2)))
        elif section_re.match(line):  # new section
            section = section_re.match(line)
            close_envs()
            lines.append('\\section{{{}}}\n'.format(section.group(1)))
        elif block_re.match(line):  # new block
            block = block_re.match(line)
            block_name = block.group(2)
            block_indent = len(block.group(1))
            close_envs(block_indent)
            lines.append(indent() + '\\begin{{block}}{{{}}}\n'.format(
                block_name))
            current_envs.append(('block', block_indent))
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
