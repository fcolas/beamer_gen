#!/usr/bin/env python3
import sys

# TODO use regular expressions


def process_file(filename_in, filename_out):
    """Actual processing of a file."""
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
            lines.append(indent() + '\\end{{{}}}'.format(env_name))

    lines = []
    current_envs = []
    for line in open(filename_in):
        if line.startswith('+ '):  # new frame
            close_envs()  # frame is always top-level environment
            lines.append('\\begin{frame}\n')
            current_envs.append('frame')
            lines.append(indent() + '\\frametitle{{{}}}\n'.format(line[2:-1]))
        else:  # default: passthrough
            lines.append(line)
    # close all remaining environments
    close_envs()
    with open(filename_out, 'w') as f_out:
        f_out.writelines(lines)


def main():
    """Command line parsing."""
    # TODO real argument parsing
    for filename_in in sys.argv[1:]:
        process_file(filename_in, filename_in+'.tex')

if __name__ == '__main__':
    main()
