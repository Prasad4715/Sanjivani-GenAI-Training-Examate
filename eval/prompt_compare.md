# ChalanCheck — Prompt Comparison Report

## 1. Objective

The objective of this evaluation is to compare two task prompt versions (`task_v1.txt` and `task_v2.txt`) for ChalanCheck, an AI-powered traffic challan explanation system.

The evaluation examines answer clarity, completeness, relevance, uncertainty handling, and consistency when explaining Indian traffic offences.

## 2. Evaluation Setup

- **LLM provider:** Google Gemini
- **Prompt versions:** V1 and V2
- **Evaluation questions:** 10
- **Total generated responses:** 20
- **Final successful responses:** 20/20
- **Source data:** ChalanCheck legal records retrieved from `data/records.json`
- **Evaluation outputs:** `eval/prompt_results.json` and `eval/prompt_review.md`

Two initial requests failed because Gemini returned HTTP 503 errors during high demand. Both were successfully retried.

## 3. Prompt Versions

### Prompt V1 — Basic Explanation

V1 asks the model to identify the relevant section, explain the offence, mention the fine and additional punishment, and respond in simple English.

Its main advantage is concise, natural explanations.

### Prompt V2 — Structured Explanation

V2 provides more detailed instructions and requires five sections:

1. Relevant Section(s)
2. Offence Explanation
3. Maximum Fine
4. Additional Action
5. Important Note

It also emphasizes explaining multiple offences separately, distinguishing statutory penalties from actual challan amounts, and avoiding unsupported calculations.

## 4. Question-wise Evaluation

| Q. No. | Test scenario | Preferred version | Observation |
|---|---|---|---|
| 1 | Helmet violation, Section 194D | V2 | Clearer separation of fine and licence action |
| 2 | Insurance violation, Section 196 | Tie | Both explain the premium-based figures, which require source verification |
| 3 | Police impounding a licence | V1 | More focused; V2 introduces unnecessary penalty details |
| 4 | Helmet and insurance combined fine | Neither | Both miss relevant records due to retrieval limitations |
| 5 | Underage driving and owner liability | Tie | Both provide partial explanations but lack juvenile-specific records |
| 6 | Sunday e-challan payment | V1 | Concise and appropriately acknowledges missing local information |
| 7 | Speeding, Section 183 | V2 | Clear vehicle-category penalties and licence consequences |
| 8 | Repeat drunk driving, Section 185 | V2 | Separates first and repeat offence penalties |
| 9 | Dangerous driving, Section 184 | Tie | Both explain the offence and additional punishments |
| 10 | Multiple sections, 194D and 196 | V2 | Better separation of violations and cautious handling of combined fines |

## 5. Findings

### Clarity

Both versions generally use understandable English. V1 is often shorter, while V2 is more organized and easier to scan.

### Completeness

V2 generally provides more complete explanations by separating legal sections, fines, additional actions, and important notes.

### Relevance

V1 performs better for some direct questions. V2 sometimes provides unnecessary details because its structure encourages filling every heading.

### Uncertainty Handling

Both prompts avoid inventing local police station opening hours and acknowledge unavailable information.

V2 more consistently includes limitations and cautions, although this can make simple answers longer.

### Legal Accuracy

The generated answers appear broadly consistent for several explicitly identified sections, but this evaluation does not independently establish legal correctness.

Some extracted legal records and penalty figures require verification against authoritative legislation.

### Retrieval Limitations

Question 4 reveals a significant retrieval problem: the system fails to identify helmet and insurance records when section numbers are absent.

This issue cannot be solved by prompt wording alone. Retrieval improvements are needed.

## 6. Final Recommendation

**Prompt V2 is selected as the default task prompt for ChalanCheck.**

Reasons:

- Consistent and readable response structure
- Clear separation of offences and penalties
- Better organization for questions involving multiple sections
- More explicit uncertainty handling
- Greater consistency for citizen-facing legal explanations

However, V2 should be improved to avoid unnecessary sections when information is irrelevant.

## 7. Future Improvements

1. Improve retrieval for everyday offence descriptions such as "no helmet" and "no insurance."
2. Add missing legal provisions, including juvenile-related sections.
3. Verify extracted fine amounts and statutory consequences against official sources.
4. Reduce unnecessary explanations for simple questions.
5. Improve confidence assessment using retrieval quality and source verification rather than answer wording alone.
6. Repeat evaluation after implementing these improvements.

## 8. Conclusion

The comparison demonstrates that prompt design affects the clarity, organization, and usefulness of ChalanCheck responses.

V2 provides a stronger default structure for explaining traffic challans, while V1 remains useful as a reference for concise answers.

The evaluation also identifies retrieval and legal-data limitations that must be addressed before relying on the system for accurate legal guidance.