# Moodle MCQ

Comvert a simple YAML file to a Moodle question bank.

## Dependancies

All dependancies are handled by
[run-in-venv](https://github.com/mthfrr/run-in-venv). Just run the python script
normaly, pypi dependancies will automaticly be installed in a venv.

## Usage

```sh
$ ./main.py -o out.xml input.yml
```

## YAML format

```yml
---
questions:
  # the default "correct" answer is the first
  - text: First question
    opt: [correct, wrong, wrong]
  - text: What is the best pet ?
    opt: [dog, cat, fish]
    # here the correct answer is `cat`
    rep: 1
    # rep index starts at 0
```

## Outputed XML

The output format is
[XML Moodle format](https://docs.moodle.org/402/en/Moodle_XML_format).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
   <question type="multichoice">
      <name>
         <text>Question 01</text>
      </name>
      <questiontext format="markdown">
         <text>First question</text>
      </questiontext>
      <answer fraction="100">
         <text>correct</text>
      </answer>
      <answer fraction="0">
         <text>wrong</text>
      </answer>
      <answer fraction="0">
         <text>wrong</text>
      </answer>
      <shuffleanswers>1</shuffleanswers>
      <single>true</single>
      <answernumbering>abc</answernumbering>
   </question>
   <question type="multichoice">
      <name>
         <text>Question 02</text>
      </name>
      <questiontext format="markdown">
         <text>What is the best pet ?</text>
      </questiontext>
      <answer fraction="0">
         <text>dog</text>
      </answer>
      <answer fraction="100">
         <text>cat</text>
      </answer>
      <answer fraction="0">
         <text>fish</text>
      </answer>
      <shuffleanswers>1</shuffleanswers>
      <single>true</single>
      <answernumbering>abc</answernumbering>
   </question>
</quiz>
```
