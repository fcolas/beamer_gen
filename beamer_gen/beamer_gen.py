#!/usr/bin/env python3
import sys
import re
import argparse
import pathlib  # python 3.4

__version__ = '1.3.0rc1'


def process_file(filename_in, filename_out):
    """Actual processing of a file."""
    # regular expressions for various directives
    frame_re = re.compile(r'^(\s*)\+((?:<[^>]*>)?)((?:\[[^\]]*\])?) ?(.*)$')
    section_re = re.compile(r'^s (.*)$')
    block_re = re.compile(r'^(\s*)b((?:<[^>]*>)?) (.*)$')
    item_re = re.compile(r'^(\s*)-((?:<[^>]*>)?)((?:\[[^\]]*\])?) (.*)$')
    enumitem_re = re.compile(r'^(\s*)#((?:<[^>]*>)?)((?:\[[^\]]*\])?) (.*)$')
    column_re = re.compile(r'^(\s*)c((?:\[[^\]]*\])?)\{([^}]*)\}(.*)$')
    figure_re = re.compile(r'^(\s*)f((?:<[^>]*>)?)\{([^}]*)\}\{([^}]*)\}(.*)$')
    empty_re = re.compile(r'^\s*$')
    end_re = re.compile(r'^\s*\\end\{[^}]*\}.*$')
    non_empty_re = re.compile(r'(\s*)\S.*$')
    # environments
    itemize_re = re.compile(r'^(\s*)\{itemize\}((?:<[^>]*>)?) ?(.*)$')
    columns_re = re.compile(r'^(\s*)\{columns\}((?:\[[^\]]*\])?)(.*)$')
    enumerate_re = re.compile(r'^(\s*)\{enumerate\}((?:<[^>]*>)?) ?(.*)$')

    def indent():
        """Return current indentation prefix."""
        try:
            return '    ' + ' ' * current_envs[-1][1]
        except IndexError:
            return ''

    def close_envs(n=0, strict=False):
        """Close currently opened environments."""
        if strict:
            n += 0.5
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
            frame_title = frame.group(4)
            frame_indent = frame.group(1)
            frame_overlay = frame.group(2)
            frame_option = frame.group(3)
            close_envs()  # frame is always top-level environment
            lines.append(frame_indent + '\\begin{{frame}}{}{}\n'.format(
                frame_overlay, frame_option))
            current_envs.append(('frame', len(frame_indent)))
            if frame_title:
                lines.append(indent() + '\\frametitle{{{}}}\n'.format(
                    frame_title))
        elif section_re.match(line):  # new section
            section = section_re.match(line)
            close_envs()
            lines.append('\\section{{{}}}\n'.format(section.group(1)))
        elif block_re.match(line):  # new block
            block = block_re.match(line)
            block_name = block.group(3)
            block_overlay = block.group(2)
            block_indent = len(block.group(1))
            close_envs(block_indent)
            lines.append(indent() + '\\begin{{block}}{}{{{}}}\n'.format(
                block_overlay, block_name))
            current_envs.append(('block', block_indent))
        elif item_re.match(line):  # new item
            item = item_re.match(line)
            item_content = item.group(4)
            item_label = item.group(3)
            item_overlay = item.group(2)
            item_indent = len(item.group(1))
            close_envs(item_indent, strict=True)
            if current_envs:
                if current_envs[-1] != ('itemize', item_indent):
                    close_envs(item_indent)
                    lines.append(indent() + '\\begin{itemize}\n')
                    current_envs.append(('itemize', item_indent))
            else:
                current_envs.append(('itemize', item_indent))
            lines.append(indent() + '\\item{}{} {}\n'.format(item_overlay,
                                                             item_label,
                                                             item_content))
        elif enumitem_re.match(line):  # new item from enumerate
            item = enumitem_re.match(line)
            item_content = item.group(4)
            item_label = item.group(3)
            item_overlay = item.group(2)
            item_indent = len(item.group(1))
            close_envs(item_indent, strict=True)
            if current_envs:
                if current_envs[-1] != ('enumerate', item_indent):
                    close_envs(item_indent)
                    lines.append(indent() + '\\begin{enumerate}\n')
                    current_envs.append(('enumerate', item_indent))
            else:
                current_envs.append(('enumerate', item_indent))
            lines.append(indent() + '\\item{}{} {}\n'.format(item_overlay,
                                                             item_label,
                                                             item_content))
        elif column_re.match(line):  # new column
            column = column_re.match(line)
            column_indent = len(column.group(1))
            column_align = column.group(2)
            column_ratio = column.group(3)
            column_rest = column.group(4)
            close_envs(column_indent, strict=True)
            if current_envs:
                if current_envs[-1] != ('columns', column_indent):
                    close_envs(column_indent)
                    lines.append(indent() + '\\begin{columns}\n')
                    current_envs.append(('columns', column_indent))
            else:
                current_envs.append(('columns', column_indent))
            lines.append(indent() + '\\column{}{{{}\\columnwidth}}{}\n'.format(
                column_align, column_ratio, column_rest))
        elif figure_re.match(line):  # figure
            figure = figure_re.match(line)
            figure_ratio = figure.group(3)
            figure_fname = figure.group(4)
            figure_rest = figure.group(5)
            figure_overlay = figure.group(2)
            lines.append(
                indent() +
                '\\includegraphics{}[width={}\\columnwidth]{{{}}}{}\n'.format(
                    figure_overlay, figure_ratio, figure_fname, figure_rest))
        elif itemize_re.match(line):  # itemize environment
            itemize = itemize_re.match(line)
            itemize_indent = len(itemize.group(1))
            itemize_overlay = itemize.group(2)
            itemize_content = itemize.group(3)
            close_envs(itemize_indent)
            lines.append(indent() + '\\begin{{itemize}}{} {}\n'.format(
                itemize_overlay,
                itemize_content))
            current_envs.append(('itemize', itemize_indent))
        elif enumerate_re.match(line):  # enumerate environment
            enumerate = enumerate_re.match(line)
            enumerate_indent = len(enumerate.group(1))
            enumerate_overlay = enumerate.group(2)
            enumerate_content = enumerate.group(3)
            close_envs(enumerate_indent)
            lines.append(indent() + '\\begin{{enumerate}}{} {}\n'.format(
                enumerate_overlay,
                enumerate_content))
            current_envs.append(('enumerate', enumerate_indent))
        elif columns_re.match(line):  # columns environment
            columns = columns_re.match(line)
            columns_indent = len(columns.group(1))
            columns_options = columns.group(2)
            columns_rest = columns.group(3)
            close_envs(columns_indent)
            lines.append(indent() + '\\begin{{columns}}{} {}\n'.format(
                columns_options, columns_rest))
            current_envs.append(('columns', columns_indent))
        else:  # default: passthrough
            non_empty = non_empty_re.match(line)
            if non_empty:
                non_empty_indent = len(non_empty.group(1))
                close_envs(non_empty_indent)
            lines.append(line)
    # close all remaining environments
    close_envs()
    # TODO handle comments at the correct indentation level
    # reorder all closing environments and empty lines
    i, N = 0, len(lines) - 1
    while i < N:
        if empty_re.match(lines[i]) and end_re.match(lines[i+1]):
            tmp = lines[i+1]
            lines[i+1] = lines[i]
            lines[i] = tmp
            i = max(0, i-1)
        else:
            i += 1
    with open(filename_out, 'w') as f_out:
        f_out.writelines(lines)


def main():
    """Command line parsing."""
    parser = argparse.ArgumentParser(
        description='Generate LaTeX/beamer files from more compact files.')
    parser.add_argument('filenames', metavar='filename', type=str, nargs='+',
                        help='name of the file to be processed.')
    args = parser.parse_args(sys.argv[1:])
    for fn in args.filenames:
        process_file(fn, str(pathlib.Path(fn).with_suffix('.tex')))


if __name__ == '__main__':
    main()
