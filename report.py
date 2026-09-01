def create_report(question, answer, sources):

    report = f"""
# Research Report

## Question

{question}

---

## Findings

{answer}

---

## Sources
"""

    unique_sources = []

    for source in sources:

        if source not in unique_sources:

            unique_sources.append(source)

    for source in unique_sources:

        report += f"\n- {source}"

    return report