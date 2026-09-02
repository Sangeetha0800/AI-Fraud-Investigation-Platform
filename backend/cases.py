import sqlite3
from datetime import datetime


DATABASE = "fraudlens.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT UNIQUE NOT NULL,
            transaction_id TEXT,
            fraud_probability REAL,
            anomaly_score REAL,
            risk_score REAL,
            risk_level TEXT,
            alert_level TEXT,
            alert_reason TEXT,
            investigation_status TEXT,
            case_status TEXT DEFAULT 'OPEN',
            investigator_notes TEXT,
            final_decision TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_case(
    transaction_id,
    fraud_probability,
    anomaly_score,
    risk_score,
    risk_level,
    alert_level,
    alert_reason
):
    conn = get_connection()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor = conn.execute("""
        INSERT INTO cases (
            case_id,
            transaction_id,
            fraud_probability,
            anomaly_score,
            risk_score,
            risk_level,
            alert_level,
            alert_reason,
            investigation_status,
            case_status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "TEMP",
        str(transaction_id),
        float(fraud_probability),
        float(anomaly_score),
        float(risk_score),
        risk_level,
        alert_level,
        alert_reason,
        "Investigation required",
        "OPEN",
        now,
        now
    ))

    case_id = f"CASE-{cursor.lastrowid:04d}"

    conn.execute("""
        UPDATE cases
        SET case_id = ?
        WHERE id = ?
    """, (case_id, cursor.lastrowid))

    conn.commit()
    conn.close()

    return case_id


def get_all_cases():
    conn = get_connection()

    cases = conn.execute("""
        SELECT *
        FROM cases
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(case) for case in cases]


def get_case(case_id):
    conn = get_connection()

    case = conn.execute("""
        SELECT *
        FROM cases
        WHERE case_id = ?
    """, (case_id,)).fetchone()

    conn.close()

    if case:
        return dict(case)

    return None


def update_case(
    case_id,
    case_status=None,
    investigator_notes=None,
    final_decision=None
):
    conn = get_connection()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn.execute("""
        UPDATE cases
        SET
            case_status = COALESCE(?, case_status),
            investigator_notes = COALESCE(?, investigator_notes),
            final_decision = COALESCE(?, final_decision),
            updated_at = ?
        WHERE case_id = ?
    """, (
        case_status,
        investigator_notes,
        final_decision,
        now,
        case_id
    ))

    conn.commit()

    updated_case = conn.execute("""
        SELECT *
        FROM cases
        WHERE case_id = ?
    """, (case_id,)).fetchone()

    conn.close()

    if updated_case:
        return dict(updated_case)

    return None