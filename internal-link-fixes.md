# procedure.tax — internal link text corrections

Scan date: 20 August 2026. All 300+ chapter HTML files scanned.

**Result:** every internal `href` already resolved to an existing file — no broken links.
The defects were in the **anchor text**: stale chapter codes from an earlier numbering
scheme, plus paraphrased chapter titles. 96 links across 67 files were rewritten to the
canonical `Code: Title` from `nav-data.js`. Any leading `See ` / `Chapter ` was preserved.

- 55 had a **wrong chapter code** (the substantive errors)
- 41 had the right code but a **non-canonical title**

Nothing else was touched: 94 insertions, 94 deletions, no net line change, `search-index.json`
unaffected. Changes are uncommitted on `main`, so `git checkout -- .` reverts everything.

---

## Wrong chapter code

| File | Was | Now |
|---|---|---|
| A01 | J8: Judicial review procedure | J9: Judicial review: procedure |
| A01 | J9: Grounds of judicial review | J10: Grounds of judicial review |
| A03 | T12: Accelerated payment notices: Reasonable excuse for not complying… | V15: Accelerated payment notices |
| A03 | Y3: Professional negligence: breach of duty | Z3: Breach of duty |
| B01 | B4: Other returns | B5: Other direct tax returns |
| C01 | See C2: Claims to recover overpaid tax | See C3: Claims to recover overpaid tax |
| D05 | T9: PAYE | V12: PAYE |
| G10 | A5: Communication | A7: Communication (notice, service etc.) |
| J02 | See J2: Challenging direct tax decisions | See J1: Appealing direct tax decision |
| J03 | See J2: Challenging direct tax decisions | See J1: Appealing direct tax decision |
| J05 | Chapter P14: (Re)payment of tax pending further appeal | Chapter R14: (Re)payment of tax pending appeal |
| J08 | M32: Imposing and relieving sanctions | P3: Relief from sanctions |
| K05 | See B10: Failure to submit a return | See B9: Failure to submit a return |
| L02 | N1: Tribunal's role (general) | Q4: Tribunal's role (general) |
| L05 | J9: Grounds of judicial review | J10: Grounds of judicial review |
| L05 | J9: Grounds of Review | J10: Grounds of judicial review |
| M03 | N1. Form and format of hearing | Q1: Form and format of hearing |
| M12 | N18: Witness evidence | Q22: Witness evidence |
| N01 | See Q13: Case management appeals | See S13: Case management appeals |
| N06 | R2: Expanding and restricting arguments on appeal | T2: New arguments on appeal |
| P03 | See Q13: Appealing case management decisions | See S13: Case management appeals |
| P06 | M30: Withdrawal | P9: Withdrawing |
| P06 | M31: Reinstatement | P10: Reinstatement of proceedings |
| P09 | Chapter M34: Settling appeals by agreement | Chapter M6: Settling appeal by agreement |
| P09 | Chapter M33: Settling appeals by agreement | Chapter M6: Settling appeal by agreement |
| P10 | N32: Imposing and relieving sanctions | P3: Relief from sanctions |
| Q04 | N8: Tribunal's role (facts) | Q9: Tribunal's role (facts) |
| Q06 | J9: Ground of judicial review | J10: Grounds of judicial review |
| Q09 | N4: Tribunal's role (general) | Q4: Tribunal's role (general) |
| Q09 | P1: Nature of Tribunal's decision | R1: Nature of Tribunal's decision |
| Q17 | M16: Amending Grounds of Appeal etc. | N6: Amending grounds of appeal etc. |
| Q18 | Q8: Bias | S10: Bias |
| Q23 | N3: Tribunal Conduct | Q3: Tribunal conduct |
| Q23 | Q9: Unfair conduct of trial | S8: Unfair conduct |
| QA07 | N2-6. Realistic view and substance | QA9: Realistic view and substance |
| QA13 | N7. Foreign law | Q8: Foreign law |
| QA13 | N2-10a: Rescission | QA14: Rescission for mistake |
| QA13 | N2-10b: Rectification | QA15: Rectification |
| R01 | N1: Tribunal's role (general) | Q4: Tribunal's role (general) |
| R04 | P6: Setting a decision aside | R6: Setting decision aside |
| R07 | M32: Imposing and relieving sanctions | P3: Relief from sanctions |
| R12 | P8: Costs in the FTT: general | R8: Costs in the FTT: general |
| R12 | P9: Costs in complex cases | R9: Costs in complex cases |
| R12 | P10: Unreasonable behaviour costs | R10: Unreasonable behaviour costs regime |
| R12 | P11: Wasted costs | R11: Wasted costs orders |
| R12 | R9: Costs on further appeal | T9: Costs on further appeal |
| S03 | Q9: Insufficient Reasons | S11: Insufficient reasons |
| S08 | N3: Tribunal conduct | Q3: Tribunal conduct |
| S08 | N19: Cross-examination | Q23: Cross-examination |
| S10 | N14: Judicial recusal | Q18: Judicial recusal |
| S10 | Q7: Unfair conduct of trial | S8: Unfair conduct |
| S10 | N8: Tribunal's Role (Facts) | Q9: Tribunal's role (facts) |
| T05 | Q11: Case management appeals | S13: Case management appeals |
| T09 | R10: protective costs orders | T10: Protective costs order etc. |
| X06 | V2: Procedure for penalties | X2: Procedure for penalty decisions |

## Correct code, title normalised

| File | Was | Now |
|---|---|---|
| A03 | See A5. Deliberate | See A5: Deliberate, fraud, dishonest |
| A06 | See G1: Direct tax assessments in general | See G1: Assessments in general (direct tax) |
| B03 | See B7: Amendment of direct tax returns | See B7: Amendment of direct tax return |
| B05 | See D1: Payment of direct tax | See D1: Payment of income tax, CGT, SDLT |
| B10 | See G4: Time limits | See G4: Time limits (direct tax) |
| C04 | See D1: Payment and repayment of income tax and CGT | See D1: Payment of income tax, CGT, SDLT |
| D01 | See B5: Other returns | See B5: Other direct tax returns |
| D02 | See D1: Payment of income tax and CGT | See D1: Payment of income tax, CGT, SDLT |
| E09 | See A3: Reasonable excuse (×2) | See A3: Reasonable, careless, capacity |
| E09 | See L4: HMRC's discretions and opinions | See L4: HMRC's discretions & opinions |
| F03 | See A7: Communication for general principles re notice | See A7: Communication (notice, service etc.) |
| F06 | Chapter J1: Challenging direct tax decisions | Chapter J1: Appealing direct tax decision |
| G04 | See A3: Reasonable excuse and carelessness | See A3: Reasonable, careless, capacity |
| G04 | See A5. Deliberate | See A5: Deliberate, fraud, dishonest |
| G04 | A3: Reasonable excuse. | A3: Reasonable, careless, capacity |
| G07 | See E4: VAT invoicing | See E4: VAT invoicing and credit notes |
| J02 | See J1: Challenging direct tax decisions | See J1: Appealing direct tax decision |
| J09 | See R15: Costs of Judicial Review | See R15: Judicial review costs |
| K02 | See J3: Appealing other indirect decisions (×2) | See J3: Appealing other indirect taxes |
| K03 | See J1: Challenging direct tax decisions | See J1: Appealing direct tax decision |
| L02 | K2: Appealable decisions (indirect tax) | K2: Indirect tax appealable decisions |
| L06 | See K1: Appealable decisions (general) | See K1: Existence of a decision |
| L10 | See N6: Amending grounds of appeal and statements of case | See N6: Amending grounds of appeal etc. |
| L10 | See P3: Imposing and relieving sanctions | See P3: Relief from sanctions |
| M06 | H5: Tax agreements pre-appeal | H5: Contract settlements |
| M13 | See Z1: Existence of duty | See Z1: Existence of duty of care |
| M14 | See M15. Third party access | See M15: Third party access to documents |
| N02 | Chapter J1: Challenging direct decisions | Chapter J1: Appealing direct tax decision |
| P07 | See K2: Appealable decisions (indirect tax) | See K2: Indirect tax appealable decisions |
| P07 | See P8: no real prospect of success | See P8: Strike out: no real prospect |
| P10 | See P9: Withdrawal | See P9: Withdrawing |
| Q10 | L2: Scope of the appeal | L2: Scope of appeal |
| R08 | See P3: Imposing and relieving sanctions | See P3: Relief from sanctions |
| S02 | See S5: Relevant and irrelevant considerations | See S5: Relevant and irrelevant consideration |
| S03 | See T3: Upper Tribunal's Role | See T3: Role of Upper Tribunal |
| S11 | See S8: Unfair conduct of trial | See S8: Unfair conduct |
| X04 | See X9: Special circumstances | See X9: Special circumstances & suspension |
| X05 | See A3: Reasonable excuse | See A3: Reasonable, careless, capacity |
| X06 | A3: Carelessness | A3: Reasonable, careless, capacity |

---

## Worth a second look

A handful of the title normalisations replaced wording that may have been deliberate —
where the link pointed at a broad chapter but the text named the specific point being
cross-referred. Check these if you want the old wording back:

- `X06` and `X05`: "A3: Carelessness" / "A3: Reasonable excuse" → now the full "A3: Reasonable, careless, capacity"
- `M06`: "H5: Tax agreements pre-appeal" → "H5: Contract settlements"
- `A03`: "T12: Accelerated payment notices: Reasonable excuse for not complying with an accelerated payment notice" → "V15: Accelerated payment notices" (the specific sub-point is lost)
- `F03`: "A7: Communication for general principles re notice" → "A7: Communication (notice, service etc.)"
- `P07`: "P8: no real prospect of success" → "P8: Strike out: no real prospect"
