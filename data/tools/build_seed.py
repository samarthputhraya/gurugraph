"""Build the GuruGraph seed data: topic pack, personas and the text evaluation set.

Run from the repo root:  python data/tools/build_seed.py
Outputs (overwritten):   data/fractions.json, data/personas.json, data/eval_text.jsonl

Every correct answer is checked with exact fraction arithmetic, and every MCQ
distractor is checked to be different from the correct value, so a typo in the
bank fails the build instead of confusing a student on stage.
"""

from __future__ import annotations

import json
import random
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CONCEPTS = [
    {"id": "C1", "name": "Equivalent fractions", "prereqs": []},
    {"id": "C2", "name": "Simplifying fractions", "prereqs": ["C1"]},
    {"id": "C3", "name": "Common denominators", "prereqs": ["C1"]},
    {"id": "C4", "name": "Adding and subtracting fractions", "prereqs": ["C3"]},
    {"id": "C5", "name": "Comparing fractions", "prereqs": ["C3"]},
    {"id": "C6", "name": "Multiplying fractions", "prereqs": ["C2"]},
    {"id": "C7", "name": "Dividing fractions", "prereqs": ["C6"]},
    {"id": "C8", "name": "Fraction word problems", "prereqs": ["C4", "C7"]},
]

TAXONOMY = [
    {"tag": "add_denominators", "definition": "Adds (or subtracts) the numerators and also the denominators, e.g. 3/4 + 1/4 = 4/8."},
    {"tag": "unlike_denominators_direct", "definition": "Combines numerators across unlike denominators without first making a common denominator, e.g. 1/2 + 1/3 = 2/6."},
    {"tag": "larger_denominator_larger", "definition": "Believes a larger denominator means a larger fraction, e.g. 1/8 > 1/4."},
    {"tag": "numerator_only_compare", "definition": "Compares fractions by their numerators alone, e.g. 3/8 > 2/3 because 3 > 2."},
    {"tag": "equivalence_additive", "definition": "Adds or subtracts the same number on top and bottom to make an 'equivalent' fraction, e.g. 2/3 = 3/4."},
    {"tag": "simplify_partial", "definition": "Scales only the numerator or only the denominator when simplifying or making equivalents, e.g. 6/8 = 3/8."},
    {"tag": "multiply_cross_add", "definition": "Mixes up the multiplication rule: cross-multiplies, or adds when it should multiply, e.g. 2/3 x 3/4 = 8/9."},
    {"tag": "multiply_common_denominator", "definition": "Makes a common denominator before multiplying, then multiplies only the numerators, e.g. 1/2 x 1/3 = 3/6 x 2/6 = 6/6."},
    {"tag": "divide_direct", "definition": "Divides without inverting the divisor, usually multiplying straight across, e.g. 3/4 / 1/4 = 3/16."},
    {"tag": "divide_flip_first", "definition": "Inverts the first fraction instead of the divisor, e.g. 3/4 / 1/4 = 4/3 x 1/4 = 1/3."},
    {"tag": "whole_number_bias", "definition": "Treats the numerator and denominator as unrelated whole numbers instead of one quantity."},
    {"tag": "word_problem_operation", "definition": "Chooses the wrong operation for a word problem, e.g. multiplies when the situation needs division."},
    {"tag": "careless_arithmetic", "definition": "Uses the right method but slips in arithmetic, or leaves the answer unsimplified when asked to simplify."},
    {"tag": "unclassified", "definition": "Cannot be classified with confidence of at least 0.5."},
]
TAGS = {t["tag"] for t in TAXONOMY}

F = Fraction


def mcq(qid, concept, stem, correct, correct_value, distractors):
    """distractors: list of (text, tag)."""
    return {
        "id": qid, "concept_id": concept, "kind": "mcq", "stem": stem,
        "options": [{"text": correct, "correct": True}] + [{"text": t, "tag": g} for t, g in distractors],
        "_value": correct_value,
    }


def text(qid, concept, stem, answer, value, method, wrong, simplest=False):
    """wrong: dict typed-answer -> tag, used for rule-first diagnosis before any LLM call.
    simplest: the stem asks for simplest form, so an equal but unsimplified answer is marked wrong."""
    return {"id": qid, "concept_id": concept, "kind": "text", "stem": stem, "answer": answer,
            "method": method, "wrong_answers": wrong, "simplest": simplest, "_value": value}


def photo(qid, concept, stem, answer, value, method):
    return {"id": qid, "concept_id": concept, "kind": "photo", "stem": stem, "answer": answer,
            "method": method, "_value": value}


QUESTIONS = [
    # C1 Equivalent fractions
    mcq("Q01", "C1", "Which fraction is equivalent to 2/3?", "4/6", F(2, 3),
        [("3/4", "equivalence_additive"), ("2/6", "simplify_partial"), ("4/9", "careless_arithmetic")]),
    mcq("Q02", "C1", "Fill in the blank: 3/5 = ?/20", "12", None,
        [("18", "equivalence_additive"), ("3", "simplify_partial"), ("15", "careless_arithmetic")]),
    mcq("Q03", "C1", "Which pair shows equivalent fractions?", "1/2 and 3/6", None,
        [("1/2 and 2/3", "equivalence_additive"), ("1/2 and 1/4", "simplify_partial"), ("1/3 and 3/1", "whole_number_bias")]),
    text("Q04", "C1", "Write a fraction equal to 3/4 that has denominator 12.", "9/12", F(3, 4),
         "3/4 = (3 x 3)/(4 x 3) = 9/12",
         {"3/12": "simplify_partial", "11/12": "equivalence_additive", "6/12": "careless_arithmetic"}),
    mcq("Q05", "C1", "Fill in the blank: 5/8 = 15/?", "24", None,
        [("18", "equivalence_additive"), ("8", "simplify_partial"), ("40", "careless_arithmetic")]),

    # C2 Simplifying
    mcq("Q06", "C2", "Simplify 6/8.", "3/4", F(3, 4),
        [("3/8", "simplify_partial"), ("2/4", "equivalence_additive"), ("2/3", "careless_arithmetic")]),
    mcq("Q07", "C2", "Write 12/18 in its lowest terms.", "2/3", F(2, 3),
        [("3/4", "careless_arithmetic"), ("4/18", "simplify_partial"), ("1/7", "equivalence_additive")]),
    text("Q08", "C2", "Write 15/25 in its simplest form.", "3/5", F(3, 5),
         "Divide top and bottom by 5: 15/25 = 3/5",
         {"3/25": "simplify_partial", "10/20": "equivalence_additive", "6/10": "careless_arithmetic"}, simplest=True),
    mcq("Q09", "C2", "Simplify 9/12.", "3/4", F(3, 4),
        [("3/12", "simplify_partial"), ("1/4", "equivalence_additive"), ("2/3", "careless_arithmetic")]),
    mcq("Q10", "C2", "Simplify 20/30.", "2/3", F(2, 3),
        [("2/30", "simplify_partial"), ("10/20", "equivalence_additive"), ("3/4", "careless_arithmetic")]),

    # C3 Common denominators
    mcq("Q11", "C3", "What is the lowest common denominator of 1/4 and 1/6?", "12", None,
        [("10", "add_denominators"), ("24", "careless_arithmetic"), ("2", "whole_number_bias")]),
    mcq("Q12", "C3", "Rewrite 2/3 and 1/4 with a common denominator.", "8/12 and 3/12", None,
        [("2/12 and 1/12", "simplify_partial"), ("2/7 and 1/7", "add_denominators"), ("8/12 and 4/12", "careless_arithmetic")]),
    text("Q13", "C3", "Find the lowest common multiple of 6 and 8.", "24", F(24),
         "Multiples of 8: 8, 16, 24; 24 is also a multiple of 6",
         {"48": "careless_arithmetic", "14": "add_denominators"}),
    mcq("Q14", "C3", "To add 1/3 + 1/5, what should the two fractions become?", "5/15 and 3/15", None,
        [("1/15 and 1/15", "simplify_partial"), ("1/8 and 1/8", "add_denominators"), ("3/15 and 5/15", "careless_arithmetic")]),
    mcq("Q15", "C3", "What is the lowest common denominator of 3/10 and 1/4?", "20", None,
        [("14", "add_denominators"), ("40", "careless_arithmetic"), ("10", "whole_number_bias")]),

    # C4 Adding and subtracting
    mcq("Q16", "C4", "3/4 + 1/4 = ?", "1", F(1),
        [("4/8", "add_denominators"), ("1/2", "add_denominators"), ("4/16", "careless_arithmetic")]),
    mcq("Q17", "C4", "1/2 + 1/3 = ?", "5/6", F(5, 6),
        [("2/5", "add_denominators"), ("2/6", "unlike_denominators_direct"), ("1/5", "careless_arithmetic")]),
    mcq("Q18", "C4", "5/6 - 1/3 = ?", "1/2", F(1, 2),
        [("4/3", "add_denominators"), ("4/6", "unlike_denominators_direct"), ("2/6", "careless_arithmetic")]),
    text("Q19", "C4", "Work out 2/5 + 1/10. Give your answer in simplest form.", "1/2", F(1, 2),
         "2/5 = 4/10; 4/10 + 1/10 = 5/10 = 1/2",
         {"5/10": "careless_arithmetic", "3/15": "add_denominators", "3/10": "unlike_denominators_direct"}, simplest=True),
    text("Q20", "C4", "Work out 3/4 - 1/6.", "7/12", F(7, 12),
         "LCM 12; 9/12 - 2/12 = 7/12",
         {"2/4": "unlike_denominators_direct", "11/12": "careless_arithmetic"}),
    photo("Q21", "C4", "On paper, work out 2/3 + 1/6 showing every step, then photograph your working.", "5/6", F(5, 6),
          "LCM of 3 and 6 is 6; 2/3 = 4/6; 4/6 + 1/6 = 5/6"),
    photo("Q22", "C4", "On paper, work out 3/4 + 1/4 showing every step, then photograph your working.", "1", F(1),
          "Same denominators: add numerators only; 3/4 + 1/4 = 4/4 = 1"),

    # C5 Comparing
    mcq("Q23", "C5", "Which is larger: 1/4 or 1/8?", "1/4", None,
        [("1/8", "larger_denominator_larger"), ("They are equal", "whole_number_bias")]),
    mcq("Q24", "C5", "Which is larger: 3/8 or 2/3?", "2/3", None,
        [("3/8", "numerator_only_compare"), ("They are equal", "careless_arithmetic")]),
    mcq("Q25", "C5", "Arrange from smallest to largest: 1/2, 1/3, 1/6", "1/6, 1/3, 1/2", None,
        [("1/2, 1/3, 1/6", "larger_denominator_larger"), ("1/3, 1/6, 1/2", "careless_arithmetic")]),
    text("Q26", "C5", "Which is greater, 5/6 or 7/9? Write the greater fraction.", "5/6", F(5, 6),
         "5/6 = 15/18 and 7/9 = 14/18, so 5/6 is greater",
         {"7/9": "numerator_only_compare"}),

    # C6 Multiplying
    mcq("Q28", "C6", "2/3 x 3/4 = ?", "1/2", F(1, 2),
        [("17/12", "multiply_cross_add"), ("8/9", "multiply_cross_add"), ("5/7", "add_denominators")]),
    mcq("Q29", "C6", "1/2 x 1/3 = ?", "1/6", F(1, 6),
        [("2/5", "add_denominators"), ("6/6", "multiply_common_denominator"), ("1/5", "multiply_cross_add")]),
    text("Q30", "C6", "Work out 3/5 x 10/9. Simplify your answer.", "2/3", F(2, 3),
         "3/5 x 10/9 = 30/45 = 2/3",
         {"30/45": "careless_arithmetic", "13/14": "add_denominators", "27/50": "multiply_cross_add"}, simplest=True),
    mcq("Q31", "C6", "What is 3/4 of 8?", "6", F(6),
        [("96", "whole_number_bias"), ("24", "careless_arithmetic"), ("3/32", "word_problem_operation")]),
    mcq("Q32", "C6", "4/5 x 5/8 = ?", "1/2", F(1, 2),
        [("9/13", "add_denominators"), ("32/25", "multiply_cross_add"), ("20/8", "careless_arithmetic")]),

    # C7 Dividing
    mcq("Q33", "C7", "3/4 / 1/4 = ?  (3/4 divided by 1/4)", "3", F(3),
        [("3/16", "divide_direct"), ("1/3", "divide_flip_first"), ("3/4", "careless_arithmetic")]),
    mcq("Q34", "C7", "2/3 divided by 4/5 = ?", "5/6", F(5, 6),
        [("8/15", "divide_direct"), ("6/5", "divide_flip_first"), ("2/5", "careless_arithmetic")]),
    text("Q35", "C7", "Work out 5/6 divided by 5/12.", "2", F(2),
         "5/6 x 12/5 = 60/30 = 2",
         {"25/72": "divide_direct", "1/2": "divide_flip_first"}),
    mcq("Q36", "C7", "How many 1/4-cup scoops are there in 3 cups?", "12", F(12),
        [("3/4", "word_problem_operation"), ("7", "whole_number_bias"), ("4", "careless_arithmetic")]),
    photo("Q37", "C7", "On paper, work out 3/5 divided by 3/10 showing every step, then photograph your working.", "2", F(2),
          "3/5 x 10/3 = 30/15 = 2"),

    # C8 Word problems
    mcq("Q38", "C8", "Ravi ate 1/3 of a pizza and Meena ate 1/4 of it. What fraction did they eat together?", "7/12", F(7, 12),
        [("2/7", "add_denominators"), ("1/12", "word_problem_operation"), ("2/12", "unlike_denominators_direct")]),
    text("Q39", "C8", "A ribbon is 3/4 m long. It is cut into pieces 1/8 m long. How many pieces?", "6", F(6),
         "3/4 divided by 1/8 = 3/4 x 8/1 = 6",
         {"3/32": "word_problem_operation", "1/6": "divide_flip_first"}),
    mcq("Q40", "C8", "A water tank is 2/3 full. Then 1/6 of the tank is used. What fraction of the tank is still full?", "1/2", F(1, 2),
        [("1/3", "add_denominators"), ("5/6", "word_problem_operation"), ("1/9", "word_problem_operation")]),
    photo("Q41", "C8", "On paper: one cake needs 3/4 cup of sugar. How much sugar do 2 cakes need? Show your steps and photograph them.", "3/2", F(3, 2),
          "2 x 3/4 = 6/4 = 3/2 = 1 1/2 cups"),
]

FRAC_RE = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s*$|^\s*(\d+)\s*$")


def parse(s: str):
    m = FRAC_RE.match(s)
    if not m:
        return None
    if m.group(3) is not None:
        return F(int(m.group(3)))
    return F(int(m.group(1)), int(m.group(2)))


def validate(questions):
    ids = [q["id"] for q in questions]
    assert len(ids) == len(set(ids)), "duplicate question ids"
    concept_ids = {c["id"] for c in CONCEPTS}
    for q in questions:
        assert q["concept_id"] in concept_ids, q["id"]
        if q["kind"] == "mcq":
            corrects = [o for o in q["options"] if o.get("correct")]
            assert len(corrects) == 1, q["id"]
            texts = [o["text"] for o in q["options"]]
            assert len(texts) == len(set(texts)), f"{q['id']}: duplicate option text"
            for o in q["options"]:
                if not o.get("correct"):
                    assert o["tag"] in TAGS, f"{q['id']}: unknown tag {o['tag']}"
            if q["_value"] is not None:
                cv = parse(corrects[0]["text"])
                assert cv == q["_value"], f"{q['id']}: correct option {corrects[0]['text']} != {q['_value']}"
                for o in q["options"]:
                    if not o.get("correct"):
                        v = parse(o["text"])
                        assert v is None or v != q["_value"], f"{q['id']}: distractor {o['text']} equals the answer"
        else:
            assert parse(q["answer"]) == q["_value"], f"{q['id']}: answer {q['answer']} != {q['_value']}"
            for wrong, tag in q.get("wrong_answers", {}).items():
                assert tag in TAGS, f"{q['id']}: unknown tag {tag}"
                if parse(wrong) == q["_value"]:
                    assert q.get("simplest"), f"{q['id']}: wrong answer {wrong} equals the answer"
    counts = {}
    for q in questions:
        counts[q["kind"]] = counts.get(q["kind"], 0) + 1
    per_concept = {c["id"]: sum(1 for q in questions if q["concept_id"] == c["id"]) for c in CONCEPTS}
    assert all(n >= 4 for n in per_concept.values()), per_concept
    return counts, per_concept


# ---------- personas ----------
NAMES = [
    "Aarav", "Ananya", "Bhavya", "Chirag", "Diya", "Farhan", "Gauri", "Harsha", "Ishita", "Jayanth",
    "Kavya", "Lakshmi", "Mohan", "Nandini", "Omkar", "Pooja", "Rahul", "Sana", "Tanvi", "Uday",
    "Varsha", "Yash", "Zoya", "Akshay", "Bindu", "Charan", "Deepa", "Eshwar", "Fathima", "Girish",
]
ARCHETYPES = {
    "solid": {
        "p_correct": {"C1": .9, "C2": .85, "C3": .8, "C4": .8, "C5": .85, "C6": .8, "C7": .6, "C8": .6},
        "preferred_tags": {"C7": "divide_direct", "C8": "word_problem_operation"},
    },
    "denominator_adder": {
        "p_correct": {"C1": .75, "C2": .7, "C3": .3, "C4": .25, "C5": .45, "C6": .65, "C7": .5, "C8": .35},
        "preferred_tags": {"C3": "add_denominators", "C4": "add_denominators", "C5": "larger_denominator_larger", "C8": "add_denominators"},
    },
    "procedure_mixer": {
        "p_correct": {"C1": .8, "C2": .7, "C3": .65, "C4": .6, "C5": .6, "C6": .3, "C7": .2, "C8": .35},
        "preferred_tags": {"C6": "multiply_cross_add", "C7": "divide_flip_first", "C8": "word_problem_operation"},
    },
}
LANGS = ["en"] * 12 + ["kn"] * 10 + ["hi"] * 8


def build_personas(seed=42):
    rng = random.Random(seed)
    langs = LANGS[:]
    rng.shuffle(langs)
    kinds = ["solid"] * 10 + ["denominator_adder"] * 11 + ["procedure_mixer"] * 9
    rng.shuffle(kinds)
    personas = []
    for i, name in enumerate(NAMES):
        a = ARCHETYPES[kinds[i]]
        jitter = {k: round(min(.97, max(.05, v + rng.uniform(-.08, .08))), 2) for k, v in a["p_correct"].items()}
        personas.append({"id": f"P{i + 1:02d}", "nickname": name, "language": langs[i], "archetype": kinds[i],
                         "p_correct": jitter, "preferred_tags": a["preferred_tags"]})
    return personas


# ---------- text evaluation set (50 typed answers, hand-labelled) ----------
EVAL = [
    ("Q04", "9/12", True, None), ("Q04", "9 / 12", True, None), ("Q04", "3/12", False, "simplify_partial"),
    ("Q04", "11/12", False, "equivalence_additive"), ("Q04", "6/12", False, "careless_arithmetic"),
    ("Q08", "3/5", True, None), ("Q08", "0.6", True, None), ("Q08", "3/25", False, "simplify_partial"),
    ("Q08", "10/20", False, "equivalence_additive"), ("Q08", "6/10", False, "careless_arithmetic"),
    ("Q13", "24", True, None), ("Q13", "48", False, "careless_arithmetic"), ("Q13", "14", False, "add_denominators"),
    ("Q13", "2", False, "unclassified"),
    ("Q19", "1/2", True, None), ("Q19", "0.5", True, None), ("Q19", "5/10", False, "careless_arithmetic"),
    ("Q19", "3/15", False, "add_denominators"), ("Q19", "3/10", False, "unlike_denominators_direct"),
    ("Q20", "7/12", True, None), ("Q20", "14/24", True, None), ("Q20", "2/4", False, "unlike_denominators_direct"),
    ("Q20", "11/12", False, "careless_arithmetic"),
    ("Q26", "5/6", True, None), ("Q26", "15/18", True, None), ("Q26", "7/9", False, "numerator_only_compare"),
    ("Q26", "they are equal", False, "careless_arithmetic"),
    ("Q30", "2/3", True, None), ("Q30", "30/45", False, "careless_arithmetic"), ("Q30", "13/14", False, "add_denominators"),
    ("Q30", "27/50", False, "multiply_cross_add"), ("Q30", "10/15", False, "careless_arithmetic"),
    ("Q35", "2", True, None), ("Q35", "2/1", True, None), ("Q35", "25/72", False, "divide_direct"),
    ("Q35", "1/2", False, "divide_flip_first"), ("Q35", "1", False, "careless_arithmetic"),
    ("Q39", "6", True, None), ("Q39", "6 pieces", True, None), ("Q39", "3/32", False, "word_problem_operation"),
    ("Q39", "1/6", False, "divide_flip_first"), ("Q39", "8", False, "unclassified"),
    ("Q17", "5/6", True, None), ("Q17", "2/5", False, "add_denominators"), ("Q17", "2/6", False, "unlike_denominators_direct"),
    ("Q29", "1/6", True, None), ("Q29", "2/5", False, "add_denominators"),
    ("Q34", "5/6", True, None), ("Q34", "8/15", False, "divide_direct"), ("Q34", "6/5", False, "divide_flip_first"),
]


def main():
    counts, per_concept = validate(QUESTIONS)
    assert len(QUESTIONS) == 40, len(QUESTIONS)
    qids = {q["id"] for q in QUESTIONS}
    for qid, _, _, tag in EVAL:
        assert qid in qids and (tag is None or tag in TAGS)
    assert len(EVAL) == 50, len(EVAL)

    public = [{k: v for k, v in q.items() if not k.startswith("_")} for q in QUESTIONS]
    pack = {"topic": {"id": "fractions_c7", "name": "Fractions (Class 7)"},
            "concepts": CONCEPTS, "taxonomy": TAXONOMY, "questions": public}
    (ROOT / "fractions.json").write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "personas.json").write_text(json.dumps(build_personas(), indent=2) + "\n", encoding="utf-8")
    with (ROOT / "eval_text.jsonl").open("w", encoding="utf-8") as fh:
        for i, (qid, ans, ok, tag) in enumerate(EVAL, 1):
            fh.write(json.dumps({"id": f"E{i:02d}", "question_id": qid, "answer": ans,
                                 "label_correct": ok, "label_tag": tag}) + "\n")
    print(f"questions: {len(QUESTIONS)} {counts}; per concept: {per_concept}; personas: 30; eval items: {len(EVAL)}")


if __name__ == "__main__":
    main()
