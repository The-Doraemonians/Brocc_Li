#set page("a4", columns: 2, numbering: "1")
#set text(font: "New Computer Modern")
#set par(justify: true, first-line-indent: 1em)
#set heading(numbering: "1.")

#place(
  top + center,
  scope: "parent",
  float: true,
  [
    Dialog Systems (MA-INF 4238) -- Summer Semester 2025

    #text(size: 14pt)[
      *Brocc Li* \
      *Your Personalized Diet Management Companion*
    ]

    #grid(
      columns: (1fr, 1fr),
      inset: (y: 5pt),
      [
        Nijat Sadikhov \
        50186266 \
        #link("mailto:s05nsadi@uni-bonn.de", "s05nsadi@uni-bonn.de")
      ],
      [
        Omar Elsebaey \
        50357345 \
        #link("mailto:s28oelse@uni-bonn.de", "s28oelse@uni-bonn.de")
      ],
      [
        Qingyu Zhao \
        50357949 \
        #link("mailto:s18qzhao@uni-bonn.de", "s18qzhao@uni-bonn.de")
      ],
      [
        Viet Dung Nguyen \
        50348141 \
        #link("mailto:s18vnguy@uni-bonn.de", "s18vnguy@uni-bonn.de")
      ],
    )

    #datetime.today().display("[month repr:long] [day], [year]")
  ],
)

#heading(numbering: none)[Abstract]

The abstract is probably what you'll be writing last, and should be roughly 300
words in length. Your abstract will get published whether or not your team wins
the challenge, so make sure to do an extra good job of it! An easy way to
structure your abstract is to write individual summaries of the four parts of
your paper (Introduction, Methods, Results, Discussion) and then put them
together once you're done.

#heading(numbering: none, level: 2)[Keywords]

pick, 3-5, good, keywords

= Introduction <sec:introduction>

Before we get to the actual introduction, welcome to Overleaf, as well as LaTeX
itself. Although LaTeX certainly has its quirks, we hope that by contrasting
the template you see here with the compiled document on the right side, you can
get an intuitive sense of how to work with it.

Another thing before the introduction; here, I'm going attach a citation to
this sentence #cite(<Goossens1994>). Scroll on down to the bibliography section
of the LaTeX code if you'd like to see the other end of the built-in references
system. The numbering is all handled in-house -- you just have to assign each
reference a key, and Overleaf takes care of the rest.

On with the actual introduction. Here is where you'd introduce the context
surrounding your study. What led you to the question you ended up asking? Why
is it relevant? Which fields of science is your question based around?

While the structure of the previous parts of the introduction can be relatively
variable, you must make sure to provide a brief overview of the study itself,
and the methods you used to accomplish it. Obviously, excessive detail is not
necessary (that's what the next section is for). Lastly, be sure to make
mention of the potential implications of your findings, but once again remember
that you'll be going into more detail about that in the discussion.

= Materials & Methods <sec:materials-and-methods>

This is where you talk about the methods used to carry out the study. Be as
concise and to-the-point as possible, and remember - *do not justify your
methods here!* You simply need to state what you did. You can (and probably
should) mention the purpose of using a certain computational tool within the
context of what you set out to achieve, but mentioning things like "it's
particularly efficient at this and better than all competing computational
tools" is unnecessary in the methods section. However, you can definitely talk
about all of this in the discussion, and talk about why your methods are, say,
the most effective ones for the task.

Think of this section as a technical manual of sorts, that another team of
researchers could read and easily follow in order to replicate what you did to
carry out this study.

Because of the straightforward nature of the methods section, this might be the
one your team wants to write first. It's essentially you just documenting what
your team has already done, which should be no problem to write, since you will
already have an established workflow by this point.

= Results <sec:results>

The results section is probably next easiest to write after the Methods
section, since it essentially boils down to presenting your data. If anything,
the production of good, high quality figures is the most important and
potentially time-consuming part of this. However, make sure to not analyze any
of your results here! All of that belongs in the discussion.

Including figures into LaTeX can seem intimidating at first, but Overleaf makes
it easy: simply click the 'Project' button above, select 'Files', and upload
away from your computer. Then, insert the file name into the appropriate
section of the code below.  Figure 1  shows the output of such code. A guide to
formatting figures can be found at
https://en.wikibooks.org/wiki/LaTeX/Floats,_Figures_and_Captions#Figures.

```tex
\begin{figure}
  \centering
  \includegraphics[width=0.4\textwidth]{test.png}
  \caption{Hello!}
\end{figure}
```

= Discussion <sec:discussion>

And here is the 'meat' of the paper, so to speak. This is where you interpret
your results, pointing out interesting trends within your data and how they
relate to your initial hypothesis. This is also the place to justify your
methodology, if you're so inclined (i.e. Why did you specifically use a certain
statistical test over another? Why this tool over that tool?). Lastly, you're
going to want to discuss potential sources of error. Make sure to make explicit
reference to figures/tables when discussing your data; it can be helpful to
walk the reader through your own personal interpretation of each figure in
order.

#heading(numbering: none)[Conclusions]

What are the long-term implications of your findings? Wrap up your discussion
succinctly while pointing out the significance of your work as well as it what
it means for the fields you examined as much as possible. Lastly, suggest ideas
for future studies that could build on your work, and justify why they might be
useful. Otherwise, you're all done!

#heading(numbering: none)[Acknowledgements]

Anyone to thank/credit for helping your team along the way? This is the place
to do it.

#bibliography("references.bib", title: "References")
