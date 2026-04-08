"""
Baseline Inference Script
Run this to test your environment locally before submitting.

Usage:
    python baseline.py
    python baseline.py --url https://your-hf-space.hf.space
"""

import argparse
import requests
import json

DEFAULT_URL = "http://localhost:7860"

TASKS = ["task_1_easy", "task_2_medium", "task_3_hard"]

BASELINE_REPLIES = {
    "task_1_easy": (
        "Hello,\n\nThank you so much for the warm welcome! "
        "I'm really happy and excited to be part of this service. "
        "Looking forward to a great experience!\n\nBest regards"
    ),
    "task_2_medium": (
        "Dear Customer,\n\nI sincerely apologize for the delay with your order #45231. "
        "This is not the experience we want for you. "
        "I will immediately look into this and help resolve the issue. "
        "Could you please share your contact details so we can assist you further?\n\n"
        "Best regards,\nSupport Team"
    ),
    "task_3_hard": (
        "Dear Customer,\n\nI sincerely apologize for the extremely poor experience with order #78932. "
        "We take full ownership of this situation — the damaged product, wrong item, and delay are "
        "completely unacceptable. I am escalating this to our priority team immediately. "
        "You will receive a full refund within 48 hours, along with compensation credit for the "
        "inconvenience caused. We deeply value your patience and will ensure this is resolved urgently.\n\n"
        "Sincerely,\nEscalations Team"
    ),
}


def run_baseline(base_url: str):
    print(f"\n🚀 Running baseline against: {base_url}\n")
    print("=" * 60)

    results = []

    for task_id in TASKS:
        print(f"\n📧 Task: {task_id}")

        # Step 1: Reset
        reset_resp = requests.post(f"{base_url}/reset", json={"task_id": task_id})
        reset_resp.raise_for_status()
        obs = reset_resp.json()
        print(f"   Subject : {obs['email_subject']}")
        print(f"   Instruction: {obs['instruction']}")

        # Step 2: Step with baseline reply
        reply = BASELINE_REPLIES[task_id]
        step_resp = requests.post(f"{base_url}/step", json={"reply": reply})
        step_resp.raise_for_status()
        result = step_resp.json()

        score = result["reward"]
        feedback = result["observation"]["feedback"]
        print(f"   ✅ Score   : {score}")
        print(f"   💬 Feedback: {feedback}")

        results.append({"task_id": task_id, "score": score})

    print("\n" + "=" * 60)
    avg = sum(r["score"] for r in results) / len(results)
    print(f"\n📊 Summary:")
    for r in results:
        print(f"   {r['task_id']}: {r['score']}")
    print(f"\n   Average Score: {avg:.2f}")
    print("\n✅ Baseline run complete!\n")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL, help="Base URL of the running environment")
    args = parser.parse_args()
    run_baseline(args.url)
