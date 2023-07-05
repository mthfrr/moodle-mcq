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
  - text: This is a shortanswer
    shortanswer:
      - bird
      - cat

  - text: Mamals
    multichoice:
      - true: cat
      - true: cow
      - bird
      - snake
      - fish

  - text: fish
    multichoice:
      - cat
      - cow
      - bird
      - snake
      - true: fish

  - text: Essay question
    essay: "do not put anything here"
```

## Outputed XML

The output format is
[XML Moodle format](https://docs.moodle.org/402/en/Moodle_XML_format).

```xml
<?xml version='1.0' encoding='utf-8'?>
<quiz>
	<question type="shortanswer">
		<name>
			<text>Question 01</text>
		</name>
		<questiontext format="markdown">
			<text>This is a shortanswer</text>
		</questiontext>
		<usecase>0</usecase>
		<answer fraction="100">
			<text>bird</text>
		</answer>
		<answer fraction="100">
			<text>cat</text>
		</answer>
	</question>
	<question type="multichoice">
		<name>
			<text>Question 02</text>
		</name>
		<questiontext format="markdown">
			<text>Mamals</text>
		</questiontext>
		<answer fraction="50.0">
			<text>cat</text>
		</answer>
		<answer fraction="50.0">
			<text>cow</text>
		</answer>
		<answer fraction="-50.0">
			<text>bird</text>
		</answer>
		<answer fraction="-50.0">
			<text>snake</text>
		</answer>
		<answer fraction="-50.0">
			<text>fish</text>
		</answer>
		<single>false</single>
		<single>false</single>
		<shuffleanswers>1</shuffleanswers>
		<answernumbering>abc</answernumbering>
	</question>
	<question type="multichoice">
		<name>
			<text>Question 03</text>
		</name>
		<questiontext format="markdown">
			<text>fish</text>
		</questiontext>
		<answer fraction="0">
			<text>cat</text>
		</answer>
		<answer fraction="0">
			<text>cow</text>
		</answer>
		<answer fraction="0">
			<text>bird</text>
		</answer>
		<answer fraction="0">
			<text>snake</text>
		</answer>
		<answer fraction="100">
			<text>fish</text>
		</answer>
		<single>true</single>
		<shuffleanswers>1</shuffleanswers>
		<answernumbering>abc</answernumbering>
	</question>
	<question type="essay">
		<name>
			<text>Question 04</text>
		</name>
		<questiontext format="markdown">
			<text>Essay question</text>
		</questiontext>
		<answer fraction="0">
			<text>do not put anything here</text>
		</answer>
	</question>
</quiz>
```
