# progress.py
import json, os, time, tempfile

LOG_DIR = "data"
LOG_FILE = os.path.join(LOG_DIR, "progress_log.json")

def _safe_load(path: str):
    """Load logs; if corrupt, back it up and start fresh."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # backup corrupt file so app keeps working
        try:
            os.rename(path, path + ".corrupt")
        except OSError:
            pass
        return []

def _atomic_write(path: str, data):
    """Atomic write to avoid partial/corrupt files."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix="progress_", suffix=".json",
                               dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass

def track_progress(name, grade, subject, topic, quiz, score):
    """
    Stores numeric fields to avoid string-mismatch bugs.
    - quiz: list of questions (for len)
    - score: number of correct answers (int)
    """
    logs = _safe_load(LOG_FILE)

    total = len(quiz) if quiz is not None else 0
    total = int(total) if total and total > 0 else 0

    # sanitize score
    try:
        correct = int(score)
    except (TypeError, ValueError):
        correct = 0

    if total > 0:
        correct = max(0, min(correct, total))  # clamp
        percent = round((correct / total) * 100, 2)
    else:
        correct, percent = 0, 0.0

    entry = {
        "name": name,
        "grade": int(grade) if str(grade).isdigit() else grade,
        "subject": subject,
        "topic": topic,
        "correct": correct,
        "total": total,
        "percent": percent,
        "ts": int(time.time())
    }

    logs.append(entry)
    _atomic_write(LOG_FILE, logs)
    return entry  # useful for UI message

def compute_overall(log_file: str = LOG_FILE):
    """
    Aggregates all attempts per student.
    Supports BOTH new schema (correct/total) and old 'score': 'x/y'.
    Returns list of dicts: {name, correct, total, percent}
    """
    logs = _safe_load(log_file)
    agg = {}

    for e in logs:
        name = e.get("name", "Unknown")

        # Prefer new numeric fields
        correct = e.get("correct")
        total = e.get("total")

        # Fallback: old schema "score": "x/y"
        if correct is None or total is None:
            s = e.get("score")
            if isinstance(s, str) and "/" in s:
                try:
                    c, t = s.split("/")
                    correct, total = int(c), int(t)
                except Exception:
                    continue
            else:
                continue

        if total is None or total < 0 or correct is None or correct < 0:
            continue

        if name not in agg:
            agg[name] = {"correct": 0, "total": 0}

        agg[name]["correct"] += correct
        agg[name]["total"] += total

    summary = []
    for name, v in agg.items():
        tot = v["total"]
        pct = round((v["correct"] / tot) * 100, 2) if tot > 0 else 0.0
        summary.append({
            "name": name,
            "correct": v["correct"],
            "total": tot,
            "percent": pct
        })
    return summary



