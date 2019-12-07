Build: [![CircleCI](https://circleci.com/gh/andrewjunyoung/symboard.svg?style=svg)](https://circleci.com/gh/andrewjunyoung/symboard)

# Ṡymβoarð (Symboard)

<!-- vim-markdown-toc GFM -->

* [About](#about)
* [Making your own keyboard](#making-your-own-keyboard)
  * [Syntax](#syntax)
    * [Setting global keyboard variables](#setting-global-keyboard-variables)
      * [List of settings](#list-of-settings)
    * [Specifying keyboard states](#specifying-keyboard-states)
      * [List of modal keys](#list-of-modal-keys)
    * [Creating dead keys](#creating-dead-keys)
* [List of keywords](#list-of-keywords)

<!-- vim-markdown-toc -->

# About

Symboard (stylized as « Ṡymβoarð ») is a versatile text-based keyboard creator.
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

In a file (we recommend using the file extension «`.symboard`»), include the
following:

The specification for keyboard files is as follows:

### Setting global keyboard variables

`<SETTING> = <VALUE>`

Example:

`KEYBOARD_TYPE = "ISO"`

There are 3 types in symboard files: strings, integers, andidentifiers
(variables). At present, is no support for higher level types.

Strings can take any unicode value, and are enclosed in double quotes (").
Double quotes within strings must be escaped using the backslash (\\).

Integers can take any integer value.

Identifiers must be declared before their usage, and will set the value of the
variable on the left to the value currently held by the variable on the right.

All settings are written using UPPER\_CAMEL\_CASE. A comprehensive list of these
can be found below.

#### List of settings
  - ` KEYBOARD\_TYPE `
  - ` LAYOUT `
 

### Specifying keyboard states

`if ( <key_condition> ) then { <key_state> }`

Example:

```
if (
  (shift? & control)
  | shift & control?)
) then {
  ~&@#$%^<>()\{\}
  :!?PYFGCRL*+|
  AOEUIDHTNS-
  "QJKXBMWVZ
}
```



#### List of modal keys
  - `shift`
  - `alt`
  - `command`
  - `control`
  - `function`
  - `caps_lock`
 

### Creating dead keys

`diacritic(<state_name>, <output_to_change>, <new_output>)`

Example:

`diacritic("acute", "abc", "áb́ć")`


# List of keywords

List of non overwriteable keywords:
  - Global program constants:
    - ` KEYBOARD\_TYPE `
    - ` LAYOUT `
  - Keyboard constants:
    - `shift`
    - `alt`
    - `command`
    - `control`
    - `function`
    - `caps_lock`
