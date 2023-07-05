#!/usr/bin/env python3

deps = ("pyyaml",)
exec(
    "N='pip'\nM='VIRTUAL_ENV'\nG='PATH'\nF='P'\nimport venv,sys,inspect as O\nfrom subprocess import check_call as P,getoutput as Q\nfrom os.path import realpath as C,dirname as R,join as D,basename as H,isdir,splitext as S\nfrom os import environ as A,execvp as T\nI=next(reversed(O.stack())).frame\nE=C(I.f_globals['__file__'])\nU=R(E)\nV=S(H(E))[0]\nB=D(U,'.'+V+'.venv')\nif M!=B:\n	if not isdir(B):A[F]=G;venv.create(B,with_pip=True)\n	J=D(B,'bin');K=C(sys.executable)\n	if K!=C(D(J,H(K))):A.update({M:B,G:J+':'+A[G]});T(E,sys.argv)\n	L=I.f_locals['deps'];[P([N,'install',*(B)])for B in(('--upgrade',N,'setuptools','wheel'),L)if F in A];[Q('pip install '+B)for B in L if F in A]"
)

import yaml, argparse
import xml.etree.ElementTree as ET
from os.path import splitext


def node(
    tag: str,
    text: str | None = None,
    attrib: dict[str, str] = {},
    children: list[ET.Element] = [],
) -> ET.Element:
    e = ET.Element(tag, **attrib)
    if text is not None:
        e.text = text
    e.extend(children)
    return e


def yaml_dumps(x) -> str:
    import io

    out = io.StringIO()
    yaml.dump(x, out)
    out.seek(0)
    return out.read()[:-1]


class Question:
    i: int
    t: str
    text: str

    def xml(self):
        return node(
            "question",
            attrib={"type": self.t},
            children=[
                node("name", children=[node("text", text=f"Question {self.i+1:02}")]),
                node(
                    "questiontext",
                    attrib={"format": "markdown"},
                    children=[node("text", self.text)],
                ),
            ],
        )


class Multichoice(Question):
    def __init__(
        self, i: int, text: str, multichoice: list, single: bool | None = None
    ):
        self.i = i
        self.text = text
        self.t = "multichoice"
        self.multichoice = multichoice
        self.single = single

    def answers(self) -> list[ET.Element]:
        res = []
        for i, c in enumerate(self.multichoice):
            if isinstance(c, str) or isinstance(c, int):
                res.append(
                    node(
                        "answer",
                        attrib={"fraction": "0"},
                        children=[node("text", str(c))],
                    )
                )
                continue
            elif isinstance(c, dict):
                if {True} == c.keys():
                    res.append(
                        node(
                            "answer",
                            attrib={"fraction": "100"},
                            children=[node("text", str(c[True]))],
                        )
                    )
                    continue

            raise Exception(
                f"Q{self.i+1:02}: R{i+1:02}: invalid format:\n{yaml_dumps(c)}"
            )

        true_answers = sum(
            1 for a in res if a.tag == "answer" and a.attrib["fraction"] == "100"
        )
        false_answers = sum(
            1 for a in res if a.tag == "answer" and a.attrib["fraction"] == "0"
        )

        if true_answers == 0:
            raise Exception(f"Q{self.i+1:02}: No answer selected")
        elif true_answers == 1:
            single = True
        else:
            single = False
            res.append(node("single", "false"))
            for a in (x for x in res if x.tag == "answer"):
                frac = a.attrib["fraction"]
                if frac == "100":
                    a.attrib["fraction"] = str(100 / true_answers)
                else:
                    a.attrib["fraction"] = str(
                        -max(100 / true_answers, 100 / false_answers)
                    )

        if self.single is None:
            self.single = single

        res.append(node("single", "true" if self.single else "false"))
        res.append(node("shuffleanswers", "1"))
        res.append(node("answernumbering", "abc"))
        return res

    def xml(self) -> ET.Element:
        res = super().xml()
        res.extend(self.answers())
        return res


class Shortanswer(Question):
    def __init__(self, i: int, text: str, shortanswer: list):
        self.i = i
        self.text = text
        self.t = "shortanswer"
        self.shortanswer = shortanswer

    def answers(self) -> list[ET.Element]:
        res = [node("usecase", "0")]
        for i, c in enumerate(self.shortanswer):
            if isinstance(c, str):
                res.append(
                    node(
                        "answer", attrib={"fraction": "100"}, children=[node("text", c)]
                    )
                )
                continue

            raise Exception(
                f"Q{self.i+1:02}: R{i+1:02}: invalid format:\n{yaml_dumps(c)}"
            )

        true_answers = sum(
            1 for a in res if a.tag == "answer" and a.attrib["fraction"] == "100"
        )

        if true_answers == 0:
            raise Exception(f"Q{self.i+1:02}: No answer selected")
        return res

    def xml(self) -> ET.Element:
        res = super().xml()
        res.extend(self.answers())
        return res


class Essay(Question):
    def __init__(self, i: int, text: str, essay: str):
        self.i = i
        self.text = text
        self.t = "essay"
        self.essay = essay

    def answers(self) -> list[ET.Element]:
        res = [
            node(
                "answer",
                attrib={"fraction": "0"},
                children=[node("text", self.essay)],
            )
        ]
        return res

    def xml(self) -> ET.Element:
        res = super().xml()
        res.extend(self.answers())
        return res


def question(i: int, **argv) -> Question:
    if "multichoice" in argv:
        return Multichoice(i, **argv)
    if "shortanswer" in argv:
        return Shortanswer(i, **argv)
    if "essay" in argv:
        return Essay(i, **argv)
    raise Exception(f"Q{i+1:02}: Unknown type\n{yaml_dumps(argv)}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-o", default=None, help="Output name")
    p.add_argument(
        "-v", "--verbose", default=False, action="store_true", help="Verbose output"
    )
    p.add_argument(
        "test",
        type=argparse.FileType("r", encoding="utf-8"),
        help="Test in yaml format",
    )
    args = p.parse_args()

    if args.o is None:
        args.o = splitext(args.test.name)[0] + ".xml"

    t = yaml.safe_load(args.test.read())
    print(f"Exporting questions: {len(t['questions'])}")

    quiz = ET.Element("quiz")
    for i, _q in enumerate(t["questions"]):
        q = question(i, **_q)
        if args.verbose:
            print(f"Question {i+1:2} ({q.t}): {q.text.splitlines()[0]}")

        q_xml = q.xml()
        if args.verbose:
            print(ET.tostring(q_xml).decode())
        quiz.append(q_xml)

        if args.verbose:
            print()

    # Export
    x = ET.ElementTree(quiz)
    x.write(args.o, encoding="utf-8", xml_declaration=True)
