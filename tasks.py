"""
6 Email Tasks (easy → hard) with multi-dimensional graders.
Each grader returns a score 0.0–1.0 based on rubrics.
"""

TASKS = {
    # ── EASY ──────────────────────────────────────────────────────────────
    "task_1_easy": {
        "task_id": "task_1_easy",
        "subject": "Welcome to Our Service!",
        "body": (
            "Hi there,\n\n"
            "Welcome! We're so glad you joined us. "
            "Feel free to reach out if you have any questions.\n\n"
            "Best,\nSupport Team"
        ),
        "instruction": (
            "Reply to this welcome email with a friendly, "
            "grateful response. Thank them for the warm welcome."
        ),
        "difficulty": "easy",
        "followup_messages": {
            "very_unhappy": "That reply didn't feel genuine at all. Can you be more personal?",
            "unhappy": "Thanks, but could you say something a bit more specific about what you're looking forward to?",
            "neutral": "Nice reply! Could you mention one thing you're excited to use the service for?",
        },
    },

    "task_2_easy": {
        "task_id": "task_2_easy",
        "subject": "Password Reset Request",
        "body": (
            "Hi,\n\n"
            "I forgot my password and can't log in. "
            "Can you help me reset it?\n\n"
            "Thanks,\nA User"
        ),
        "instruction": (
            "Reply professionally. Guide them through the password reset process. "
            "Be clear, step-by-step, and reassuring."
        ),
        "difficulty": "easy",
        "followup_messages": {
            "very_unhappy": "I still don't understand what to do. Can you explain step by step?",
            "unhappy": "Where exactly do I click? I can't find the reset button.",
            "neutral": "Got it, but what if I don't receive the reset email?",
        },
    },

    # ── MEDIUM ────────────────────────────────────────────────────────────
    "task_3_medium": {
        "task_id": "task_3_medium",
        "subject": "My order has not arrived yet!",
        "body": (
            "Hello,\n\n"
            "I placed an order 10 days ago (Order #45231) and it still hasn't arrived. "
            "This is unacceptable! I need this urgently. "
            "What is going on?\n\n"
            "Regards,\nAngry Customer"
        ),
        "instruction": (
            "Reply to this complaint email professionally and empathetically. "
            "Apologize, reference the order number, and offer to resolve the issue."
        ),
        "difficulty": "medium",
        "followup_messages": {
            "very_unhappy": "Your reply is useless! You didn't even check where my order is. Fix this NOW!",
            "unhappy": "I need more than an apology — what are you actually going to DO about order #45231?",
            "neutral": "Okay, I'll wait. But what is the expected delivery date now?",
        },
    },

    "task_4_medium": {
        "task_id": "task_4_medium",
        "subject": "Wrong item delivered",
        "body": (
            "Hello Support,\n\n"
            "I ordered a blue jacket (Size M) but received a red one in Size XL. "
            "Order number: #99312. This is clearly a packing error. "
            "Please arrange an exchange as soon as possible.\n\n"
            "Best,\nA Customer"
        ),
        "instruction": (
            "Reply professionally. Acknowledge the packing error, apologize sincerely, "
            "confirm you will arrange an exchange, and give a clear next step."
        ),
        "difficulty": "medium",
        "followup_messages": {
            "very_unhappy": "You still haven't told me HOW to return the wrong item. What do I do with it?",
            "unhappy": "When exactly will I receive the correct jacket? I need a date.",
            "neutral": "Do I need to pay for return shipping, or will you cover it?",
        },
    },

    # ── HARD ──────────────────────────────────────────────────────────────
    "task_5_hard": {
        "task_id": "task_5_hard",
        "subject": "Requesting Full Refund + Compensation",
        "body": (
            "To Whom It May Concern,\n\n"
            "I am writing to formally request a full refund for Order #78932. "
            "The product arrived damaged, 3 weeks late, and was the wrong item entirely. "
            "I have already contacted support twice with no resolution. "
            "I expect a full refund AND compensation for my time and inconvenience. "
            "If this is not resolved within 48 hours, I will escalate to consumer court "
            "and post a public review.\n\n"
            "Sincerely,\nFrustrated Customer"
        ),
        "instruction": (
            "Reply professionally. Take full ownership, confirm the refund, "
            "offer compensation, and give a specific timeline. Be empathetic."
        ),
        "difficulty": "hard",
        "followup_messages": {
            "very_unhappy": "This is the THIRD time I've been given empty promises. I want a manager!",
            "unhappy": "You said refund but didn't say HOW MUCH or WHEN. Be specific.",
            "neutral": "I appreciate the response. Can you confirm the refund in writing via email?",
        },
    },

    "task_6_hard": {
        "task_id": "task_6_hard",
        "subject": "Threatening legal action over data breach",
        "body": (
            "Dear Support,\n\n"
            "I have been informed by my bank that my credit card details may have been "
            "compromised through your platform. I have not authorized any recent transactions "
            "totaling $320. I demand an immediate explanation, confirmation of whether a breach "
            "occurred, and full reimbursement. If I do not hear back within 24 hours with a "
            "concrete response, I will be contacting my attorney and filing a complaint with "
            "the relevant data protection authority.\n\n"
            "Regards,\nConcerned Customer"
        ),
        "instruction": (
            "Reply to this urgent security/legal complaint. Acknowledge the severity, "
            "don't dismiss the claim, take it seriously, explain what steps you'll take, "
            "and offer direct escalation to your security team. Be professional and calm."
        ),
        "difficulty": "hard",
        "followup_messages": {
            "very_unhappy": "This generic reply is insulting. Was there a breach or NOT? Answer directly.",
            "unhappy": "You mentioned an investigation but gave no timeline. When will I get answers?",
            "neutral": "Thank you. Can you give me a reference number for this complaint so I can track it?",
        },
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Grading Logic — Multi-dimensional rubrics (not just keyword matching)
# ─────────────────────────────────────────────────────────────────────────────

def grade_reply(task_id: str, reply: str) -> tuple[float, str]:
    """
    Grade the agent's reply using a multi-dimensional rubric.
    Each dimension is scored independently and weighted.
    Returns (score: float 0.0–1.0, feedback: str)
    """
    reply_lower = reply.lower().strip()
    feedback_parts = []

    if not reply or len(reply_lower) < 20:
        return 0.0, "Reply is too short or empty."

    graders = {
        "task_1_easy":   _grade_task1,
        "task_2_easy":   _grade_task2_easy,
        "task_3_medium": _grade_task3_medium,
        "task_4_medium": _grade_task4_medium,
        "task_5_hard":   _grade_task5_hard,
        "task_6_hard":   _grade_task6_hard,
    }

    if task_id not in graders:
        return 0.0, f"Unknown task_id: {task_id}"

    score = graders[task_id](reply_lower, feedback_parts)

    # Universal quality bonus: proper greeting + sign-off
    if any(w in reply_lower for w in ["dear", "hello", "hi", "good morning", "good afternoon"]):
        score = min(score + 0.03, 1.0)
    if any(w in reply_lower for w in ["sincerely", "regards", "best wishes", "warm regards", "thank you"]):
        score = min(score + 0.02, 1.0)

    feedback = " | ".join(feedback_parts) if feedback_parts else "Excellent reply!"
    return round(min(max(score, 0.0), 1.0), 2), feedback


def _score_dimension(reply: str, keywords: list, weight: float, label: str, feedback: list) -> float:
    """Generic dimension scorer."""
    if any(w in reply for w in keywords):
        return weight
    feedback.append(f"Missing: {label}")
    return 0.0


def _grade_task1(reply: str, feedback: list) -> float:
    """Easy: friendly thank-you reply."""
    score = 0.0
    score += _score_dimension(reply, ["thank", "thanks", "grateful", "appreciate"], 0.35, "gratitude", feedback)
    score += _score_dimension(reply, ["happy", "glad", "excited", "looking forward", "thrilled", "delighted"], 0.25, "enthusiasm", feedback)
    score += _score_dimension(reply, ["hello", "hi", "dear", "greetings"], 0.15, "greeting", feedback)
    if len(reply) > 50: score += 0.15
    else: feedback.append("Too brief")
    if len(reply) <= 500: score += 0.10
    else: feedback.append("Too long for a welcome reply")
    return score


def _grade_task2_easy(reply: str, feedback: list) -> float:
    """Easy: password reset guidance."""
    score = 0.0
    score += _score_dimension(reply, ["reset", "password", "link", "email", "forgot"], 0.30, "addresses password reset", feedback)
    score += _score_dimension(reply, ["step", "click", "go to", "visit", "navigate", "follow"], 0.25, "step-by-step guidance", feedback)
    score += _score_dimension(reply, ["help", "assist", "support", "happy to"], 0.20, "willingness to help", feedback)
    if len(reply) > 80: score += 0.15
    else: feedback.append("Needs more detail")
    score += _score_dimension(reply, ["issue", "problem", "concern", "trouble", "question"], 0.10, "acknowledges issue", feedback)
    return score


def _grade_task3_medium(reply: str, feedback: list) -> float:
    """Medium: delayed order complaint."""
    score = 0.0
    score += _score_dimension(reply, ["sorry", "apologize", "apologies", "regret"], 0.25, "apology", feedback)
    score += _score_dimension(reply, ["45231", "order", "shipment", "delivery", "package"], 0.20, "references order", feedback)
    score += _score_dimension(reply, ["resolve", "fix", "help", "assist", "look into", "investigate", "check"], 0.20, "action offered", feedback)
    score += _score_dimension(reply, ["contact", "reach", "detail", "information", "update", "track"], 0.15, "requests/offers info", feedback)
    if len(reply) > 100: score += 0.10
    else: feedback.append("Too brief for a complaint")
    score += _score_dimension(reply, ["urgency", "urgent", "priority", "immediately", "soon", "quickly", "asap"], 0.10, "acknowledges urgency", feedback)
    return score


def _grade_task4_medium(reply: str, feedback: list) -> float:
    """Medium: wrong item delivered."""
    score = 0.0
    score += _score_dimension(reply, ["sorry", "apologize", "apologies", "error", "mistake"], 0.25, "apology/acknowledges error", feedback)
    score += _score_dimension(reply, ["exchange", "replace", "correct item", "send", "dispatch", "ship"], 0.25, "offers exchange/replacement", feedback)
    score += _score_dimension(reply, ["99312", "order", "blue", "jacket", "wrong item"], 0.20, "references specifics", feedback)
    score += _score_dimension(reply, ["return", "pick up", "collect", "send back", "label"], 0.15, "explains return process", feedback)
    if len(reply) > 100: score += 0.15
    else: feedback.append("Too brief")
    return score


def _grade_task5_hard(reply: str, feedback: list) -> float:
    """Hard: escalated refund + compensation."""
    score = 0.0
    score += _score_dimension(reply, ["sincerely apologize", "deeply sorry", "truly sorry", "sorry", "apologize"], 0.18, "strong apology", feedback)
    score += _score_dimension(reply, ["refund", "reimburse", "return", "money back"], 0.18, "addresses refund", feedback)
    score += _score_dimension(reply, ["compensat", "credit", "voucher", "discount", "goodwill"], 0.17, "offers compensation", feedback)
    score += _score_dimension(reply, ["48 hours", "24 hours", "immediately", "priority", "urgent", "escalat"], 0.15, "specific timeline", feedback)
    score += _score_dimension(reply, ["ownership", "responsibility", "our fault", "our mistake", "we take", "accountab"], 0.12, "takes ownership", feedback)
    score += _score_dimension(reply, ["78932", "damaged", "wrong", "delay", "three", "twice"], 0.10, "references specifics", feedback)
    if len(reply) > 150: score += 0.10
    else: feedback.append("Too brief for escalation")
    return score


def _grade_task6_hard(reply: str, feedback: list) -> float:
    """Hard: security breach + legal threat."""
    score = 0.0
    score += _score_dimension(reply, ["serious", "urgently", "immediately", "priority", "severity", "understand your concern"], 0.20, "acknowledges seriousness", feedback)
    score += _score_dimension(reply, ["security", "breach", "investigate", "review", "look into", "data"], 0.20, "addresses security concern", feedback)
    score += _score_dimension(reply, ["320", "transaction", "charge", "unauthorized", "reimburs", "refund"], 0.18, "addresses financial concern", feedback)
    score += _score_dimension(reply, ["team", "specialist", "escalate", "security team", "department"], 0.15, "escalates to specialist", feedback)
    score += _score_dimension(reply, ["24 hours", "immediately", "soon", "priority", "timeline", "update"], 0.12, "gives timeline", feedback)
    score += _score_dimension(reply, ["reference", "ticket", "case number", "complaint id", "track"], 0.05, "provides reference", feedback)
    if len(reply) > 150: score += 0.10
    else: feedback.append("Too brief for a legal/security complaint")
    return score
