Build: [![CircleCI](https://circleci.com/gh/andrewjunyoung/symboard.svg?style=svg)](https://circleci.com/gh/andrewjunyoung/symboard)

# Ṡymβoarð (Symboard)

<!-- vim-markdown-toc GFM -->

* [About](#about)
* [Making your own keyboard](#making-your-own-keyboard)
  * [Syntax](#syntax)
* [Future features](#future-features)
  * [Specifying keyboard states (not yet implemented)](#specifying-keyboard-states-not-yet-implemented)
    * [List of modal keys](#list-of-modal-keys)
  * [Creating dead keys (not yet implemented)](#creating-dead-keys-not-yet-implemented)

<!-- vim-markdown-toc -->

# About

Symboard (stylized as «Ṡymβoarð») is a versatile text-based keyboard creator.
Symboard has a defined syntax which allows you to create text files which
describe the specification for a keyboard layout, and will compile these files
to automatically create a fully functional, UNIX compatible `keylayout` file.

The syntax of Symboard (described below) currently allows for 3 different type
of operation:
- Setting global keyboard variables, such as keyboard type and layout
- Specifying different keyboard states, such as shift, or alt
- A concise syntax to create dead keys, such as for accents and diacritics.

# Making your own keyboard

## Syntax

Symboard creates keyboards according to a _specification_ (spec) which is provided to it. This spec should be written as a [yaml](https://en.wikipedia.org/wiki/YAML) file.

Yaml can be a little technical at times, so here's what you need to know when using symboard.

Yaml is made up of keys (headers) which point to values, like this:

```
given_name: noam
surname: chomsky
age: 91
institutions:
    - University of Arizona
      start: 2017
    - Massachusetts Institute of Technology
      start: 1955
    - Institute for Advanced Study
      start: 1958
      end: 1959
```

Values can be numbers, strings, booleans (true / false), or lists.

Symboard has some required headings, while others are optional. Optional headings, if not included in your specification, will be set to some default value. This default value is usually picked to be the most appropriate for the keyboard layout you're trying to create.

Which headings are available, and which are required, is detailed [here](https://github.com/andrewjunyoung/symboard/wiki/Symboard-yaml-syntax) in the symboard wiki. All symboard settings are written using lower_camel_case.

# Future features

## Specifying keyboard states (not yet implemented)

```
keyboard_state:
  condition: ...
  state: |
    ...
```

Example:

```
keyboard_state:
  condition: (shift? & control) | shift & control?)
  state: |
    ~&@#$%^<>()\{\}
    :!?PYFGCRL*+|
    AOEUIDHTNS-
    "QJKXBMWVZ
```

### List of modal keys
  - `shift`
  - `alt`
  - `command`
  - `control`
  - `function`
  - `caps_lock`


## Creating dead keys (not yet implemented)

```
dead_key:
  name: ...
  modified_from: ...
  modified_to: ...
```

Example:


```
dead_key:
  name: acute
  modified_from: abc
  modified_to: áb́ć
```
