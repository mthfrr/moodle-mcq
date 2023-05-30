#!/usr/bin/env python3

deps = ("pyyaml",)
exec(
    "N='pip'\nM='VIRTUAL_ENV'\nG='PATH'\nF='P'\nimport venv,sys,inspect as O\nfrom subprocess import check_call as P,getoutput as Q\nfrom os.path import realpath as C,dirname as R,join as D,basename as H,isdir,splitext as S\nfrom os import environ as A,execvp as T\nI=next(reversed(O.stack())).frame\nE=C(I.f_globals['__file__'])\nU=R(E)\nV=S(H(E))[0]\nB=D(U,'.'+V+'.venv')\nif M!=B:\n	if not isdir(B):A[F]=G;venv.create(B,with_pip=True)\n	J=D(B,'bin');K=C(sys.executable)\n	if K!=C(D(J,H(K))):A.update({M:B,G:J+':'+A[G]});T(E,sys.argv)\n	L=I.f_locals['deps'];[P([N,'install',*(B)])for B in(('--upgrade',N,'setuptools','wheel'),L)if F in A];[Q('pip install '+B)for B in L if F in A]"
)

import yaml, argparse
import xml.etree.ElementTree as ET
from dataclasses import dataclass


@dataclass
class Question:
    text: str
    opt: list[str]  # available answers
    rep: int = 0  # index of correct response


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


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-o", default="out.xml", help="Output name")
    p.add_argument(
        "-v", "--verbose", default=False, action="store_true", help="Verbose output"
    )
    p.add_argument(
        "test",
        type=argparse.FileType("r", encoding="utf-8"),
        help="Test in yaml format",
    )
    args = p.parse_args()

    t = yaml.safe_load(args.test.read())
    print(f"Exporting questions: {len(t['questions'])}")

    quiz = ET.Element("quiz")
    for i, q_dict in enumerate(t["questions"]):
        q = Question(**q_dict)

        if args.verbose:
            print(f"Question {i+1:2}: {q.text.splitlines()[0]}")

        quiz.append(
            node(
                "question",
                attrib={"type": "multichoice"},
                children=[
                    node("name", children=[node("text", text=f"Question {i+1:02}")]),
                    node(
                        "questiontext",
                        attrib={"format": "markdown"},
                        children=[node("text", q.text)],
                    ),
                    *[
                        node(
                            "answer",
                            attrib={"fraction": "100" if q.rep == i else "0"},
                            children=[node("text", str(a))],
                        )
                        for (i, a) in enumerate(q.opt)
                    ],
                    node("shuffleanswers", "1"),
                    node("single", "true"),
                    node("answernumbering", "abc"),
                ],
            )
        )

    # Export
    x = ET.ElementTree(quiz)
    x.write(args.o, encoding="utf-8", xml_declaration=True)
