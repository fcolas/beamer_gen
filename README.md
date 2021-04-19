beamer_gen
==========

Preprocessor to generate LaTeX-beamer code from a more compact language.

The needs for a new sub language were:

- compactness: so as to type as few formatting informations as possible,
- expressiveness: allow to format most beamer frames with clear and short syntax,
- flexibility: allowance for LaTeX without too much overhead.

In TeX, environments are enclosed into ``\begin{env}`` and ``\end{env}`` tags which makes it unambiguous but requires duplicating the name of the environment.
Here, for compactness, the choice is made instead to use indentation as environment markers.
Indentation is therefore significant and compulsory.


Features
--------

``beamer_gen`` code has shortcuts for the following current LaTeX/beamer features:

- sections, using ``s Section title``,
- frames, using ``+ Frame title``,
- blocks, using ``b Block title``,
- itemize, using ``- item text`` with automatic environment creation,
- enumerate, using ``# item text`` with automatic environment creation,
- columns, using ``c{ratio}`` (ratio relative to ``\columnwidth``) with automatic environment creation,
- figures, using ``f{ratio}{filename}`` (ratio relative to ``\columnwidth``).

In addition, options can be placed to some environments that are implicitly defined by inserting them before:

- itemize, using ``{itemize} commands``
- columns, using ``{columns}[options]``


Beamer overlay directives (``<...>``) are supported for most elements.
Frames and items can also have options (``[...]``), in which case, they must be specified after an optional beamer directive (``+<+->[fragile] Title``, or ``-<+->[\square] item`` for instance).
Columns can also have a placement option (e.g. ``[c]``), which needs to be specified before the size.

Everything else is reproduced verbatim.


Usage
-----

Usage is straightforward:

    usage: beamer_gen.py [-h] filename [filename ...]

    Generate LaTeX/beamer files from a stub.

    positional arguments:
      filename    name of the file to be processed.

    optional arguments:
      -h, --help  show this help message and exit

Each file is processed by creating a new file with the original extension replaced by ``.tex``.


Example
-------

The following source:

```
+[allowframebreaks] Example 1
    b<+-> Example block
        - first item
            # subitem in enumerate
            # other subitem
        - second item
        -<2>[!] third item
    b<+-> second block
        {columns}[T]
        c{0.4}
            f<3->{0.8}{figure1.png}
        c[t]{0.6}
            Some generic text:
            {itemize}<+-> \itemsep 1.5em
            - and
            - items
            {enumerate}<+->
            # and numbered
            # items
```

translates into:

```tex
\begin{frame}[allowframebreaks]
    \frametitle{Example 1}
    \begin{block}<+->{Example block}
        \begin{itemize}
            \item first item
            \begin{enumerate}
                \item subitem in enumerate
                \item other subitem
            \end{enumerate}
            \item second item
            \item<2>[!] third item
        \end{itemize}
    \end{block}
    \begin{block}<+->{second block}
        \begin{columns}[T]
            \column{0.4\columnwidth}
            \includegraphics<3->[width=0.8\columnwidth]{figure1.png}
            \column[t]{0.6\columnwidth}
            Some generic text:
            \begin{itemize}<+-> \itemsep 1.5em
                \item and
                \item items
            \end{itemize}
            \begin{enumerate}<+->
                \item and numbered
                \item items
            \end{enumerate}
        \end{columns}
    \end{block}
\end{frame}
```
