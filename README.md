# Hooktheory Latent Statistics Toolkit (HoLST)
HoLST is a novice-friendly toolkit for completing corpus analysis of songs featured on [Hooktheory](https://www.hooktheory.com/site), a user-contributed website where users transcribe the theoretical backbone of popular songs. This toolkit can read and parse Hooktheory's .hkt file format and extract meaningful information and statistics from the melodies and harmonies inside.

# Motivation
The main motivation for HoLST was the creation of a new course at the University of Delaware - **MUSC106: Computational Thinking in Music**. At this point in time, the University recently received an NSF grant to implement *computational thinking* into general education courses. We wanted a piece of software that would easily parse data from Hooktheory (one of the largest music theory databases available right now) and produce relevant statistics.

As we quickly learned (as of date), Hooktheory's own API is seriously lacking in utility. It does not support the ability to search by artist, by song name, by key or mode, etc. The only tool provided is to search for songs with the same progression (and analysis of the entire Hooktheory corpus has been done many times before). This meant that our users had to download the .hkt files themselves, which unfortunately requires a Hooktheory Plus membership.

One of the main goals we had in mind was for the Toolkit to be friendly to beginning programmers, since the function of the course was to introduce students to the main concepts of programming and Computer Science through the lens of music theory.

# Features
* Parses .hkt files and encapsulates the XML parameters into Objects
* Statistical analysis of the corpus, such as melody, harmony, and rhythm
* Statistically influenced generation of harmonic progressions, melodic figures, and rhythm vectors
* Graphing functionality using Plotly

# How to Use
```python
import analysis_model as analysis

obj = analysis.CorpusAnalysis("path/to/corpus/folder")
print(obj.generate_progression())
```
# Issues
* Currently the model works best in 4/4, detailed support for other time signatures will be avalible in the future
* Due to Hooktheory's questionable method of handling borrowed chords, in rare cases the algorithm will be unable to identify a chord if the mode is changed from the the song's original
