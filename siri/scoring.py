from typing import Dict, List
from .models import Question, Dimension, AssessmentResult, DimensionScore, PillarScore


def compute_scores(answers: Dict[str, float], questions: List[Question], dimensions: List[Dimension]) -> AssessmentResult:
    # Map helpers
    q_by_id = {q.id: q for q in questions}
    dim_by_id = {d.id: d for d in dimensions}

    # Aggregate per dimension
    dim_acc: Dict[str, List[float]] = {}
    for qid, score in answers.items():
        q = q_by_id.get(qid)
        if not q:
            continue
        dim_id = q.dimension_id
        dim_acc.setdefault(dim_id, []).append(float(score))

    dim_scores: List[DimensionScore] = []
    for dim in dimensions:
        scores = dim_acc.get(dim.id, [])
        avg = sum(scores) / len(scores) if scores else 0.0
        dim_scores.append(DimensionScore(dimension_id=dim.id, dimension_name=dim.name, pillar=dim.pillar, score=round(avg, 2)))

    # Pillar aggregation (weighted by dimension weight)
    pillar_groups: Dict[str, List[float]] = {}
    for ds in dim_scores:
        pillar_groups.setdefault(ds.pillar, []).append(ds.score)

    pillars: List[PillarScore] = []
    for pillar, vals in pillar_groups.items():
        avg = sum(vals) / len(vals) if vals else 0.0
        pillars.append(PillarScore(pillar=pillar, score=round(avg, 2)))

    # Overall
    all_dim_vals = [ds.score for ds in dim_scores]
    overall = sum(all_dim_vals) / len(all_dim_vals) if all_dim_vals else 0.0

    # Simple rule-based recommendations (example)
    recs: List[str] = []
    low_dims = [ds for ds in dim_scores if ds.score < 2.0]
    for ds in low_dims[:3]:
        if ds.pillar == "Technology":
            recs.append(f"تعزيز القدرات التقنية في بُعد {ds.dimension_name} (بدءًا بمشروعات محدودة النطاق PoC).")
        elif ds.pillar == "Process":
            recs.append(f"تحسين العمليات وربط البيانات في بُعد {ds.dimension_name} من المصدر إلى لوحة القياس.")
        else:
            recs.append(f"رفع جاهزية التنظيم والمهارات في بُعد {ds.dimension_name} عبر تدريب مستهدف وحوكمة واضحة.")

    return AssessmentResult(
        session_id="",
        overall_score=round(overall, 2),
        pillars=sorted(pillars, key=lambda x: x.pillar),
        dimensions=sorted(dim_scores, key=lambda x: (x.pillar, x.dimension_name)),
        recommendations=recs,
    )

