from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(r"C:\Users\dodo\Documents\Codex\ACG_AI_picture")
SHEET = ROOT / "logs" / "checkpoint_evaluation_sheet_senren_banka_asatake_yoshino.csv"

scores = {
    1000: {
        1: (5, 4, 4, 5, 4, 3, 3, "Strong close-up; identity is solid."),
        2: (4, 4, 4, 4, 4, 3, 3, "Good upper-body control."),
        3: (3, 3, 3, 3, 3, 3, 4, "Full-body still a bit stiff."),
        4: (3, 3, 3, 3, 3, 3, 4, "Side-angle identity is weaker."),
        5: (3, 3, 3, 3, 3, 3, 4, "Looking-back pose is acceptable but not strong."),
        6: (4, 4, 4, 4, 4, 3, 3, "Seated framing is stable."),
        7: (3, 3, 3, 3, 3, 3, 4, "Motion is present but not especially flexible."),
        8: (4, 4, 4, 4, 4, 3, 3, "Emotion range is decent."),
        9: (4, 4, 4, 4, 4, 4, 3, "Outfit variation holds better than the weaker poses."),
        10: (2, 1, 1, 2, 2, 1, 4, "Not a true inpaint test in the current workflow."),
    },
    1200: {
        1: (5, 5, 5, 5, 5, 3, 3, "Excellent close-up identity."),
        2: (4, 4, 4, 4, 4, 4, 3, "Solid full-body framing."),
        3: (5, 5, 5, 5, 4, 4, 3, "Best motion result of the set."),
        4: (4, 4, 4, 4, 4, 4, 3, "Side view is usable."),
        5: (5, 5, 4, 5, 4, 4, 3, "Looking-back pose stays recognizably Yoshino."),
        6: (4, 4, 4, 4, 4, 4, 3, "Seated scene is steady."),
        7: (4, 5, 5, 4, 4, 4, 3, "Motion is strong and readable."),
        8: (5, 5, 5, 5, 4, 4, 3, "Expression range is strong."),
        9: (2, 4, 4, 4, 4, 4, 2, "Identity drifted into a red-haired character."),
        10: (3, 2, 2, 3, 3, 2, 3, "Baseline only; not a true inpaint workflow."),
    },
}

with SHEET.open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    ckpt = int(row["checkpoint"])
    test_id = int(row["test_id"])
    if ckpt in scores and test_id in scores[ckpt]:
        ident, prompt, pose, face, hands, outfit, overfit, notes = scores[ckpt][test_id]
        row["identity_1_5"] = str(ident)
        row["prompt_follow_1_5"] = str(prompt)
        row["pose_1_5"] = str(pose)
        row["face_1_5"] = str(face)
        row["hands_body_1_5"] = str(hands)
        row["outfit_flex_1_5"] = str(outfit)
        row["overfit_risk_1_5"] = str(overfit)
        row["notes"] = notes

with SHEET.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"updated {SHEET}")
