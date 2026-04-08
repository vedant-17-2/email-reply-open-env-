

import uuid
from models import EmailAction, EmailObservation, EpisodeState, ConversationTurn
from tasks import TASKS, grade_reply

MAX_TURNS = 3


class EmailReplyEnvironment:
    def __init__(self):
        self._episode_id: str = ""
        self._step_count: int = 0
        self._current_task_id: str = ""
        self._done: bool = False
        self._last_score: float = 0.0
        self._turn_number: int = 0
        self._cumulative_score: float = 0.0
        self._conversation_history: list = []

    def reset(self, task_id: str = "task_1_easy") -> EmailObservation:
        """Start a new episode with the given task."""
        if task_id not in TASKS:
            task_id = "task_1_easy"

        self._episode_id = str(uuid.uuid4())
        self._step_count = 0
        self._current_task_id = task_id
        self._done = False
        self._last_score = 0.0
        self._turn_number = 0
        self._cumulative_score = 0.0
        self._conversation_history = []

        task = TASKS[task_id]

        # First customer message is the original email body
        first_msg = ConversationTurn(role="customer", message=task["body"])
        self._conversation_history.append(first_msg)

        return EmailObservation(
            email_subject=task["subject"],
            email_body=task["body"],
            task_id=task_id,
            instruction=task["instruction"],
            conversation_history=list(self._conversation_history),
            current_customer_message=task["body"],
            turn_number=self._turn_number,
            done=False,
        )

    def step(self, action: EmailAction) -> tuple[EmailObservation, float, bool]:
        """
        Execute one step: evaluate the agent's reply.
        If the score is low and turns remain, the customer
        sends a follow-up — the episode continues.
        Returns (observation, reward, done)
        """
        if self._done:
            raise ValueError("Episode is done. Call reset() to start a new episode.")

        self._step_count += 1
        self._turn_number += 1
        task = TASKS[self._current_task_id]

        score, feedback = grade_reply(self._current_task_id, action.reply)
        self._last_score = score
        self._cumulative_score += score

        # Record agent reply
        agent_turn = ConversationTurn(role="agent", message=action.reply, score=score)
        self._conversation_history.append(agent_turn)

        # Decide if episode ends or customer follows up
        customer_followup = None
        if score >= 0.75 or self._turn_number >= MAX_TURNS:
            # Customer satisfied or max turns reached
            self._done = True
        else:
            # Customer sends a follow-up based on dissatisfaction level
            customer_followup = self._get_customer_followup(score)
            customer_turn = ConversationTurn(role="customer", message=customer_followup)
            self._conversation_history.append(customer_turn)

        # Final reward = average score across all turns
        final_reward = round(self._cumulative_score / self._turn_number, 3)

        observation = EmailObservation(
            email_subject=task["subject"],
            email_body=task["body"],
            task_id=self._current_task_id,
            instruction=task["instruction"],
            conversation_history=list(self._conversation_history),
            current_customer_message=customer_followup,
            turn_number=self._turn_number,
            last_reply=action.reply,
            score=score,
            feedback=feedback,
            done=self._done,
        )
        return observation, final_reward, self._done

    def _get_customer_followup(self, score: float) -> str:
        """Generate a realistic customer follow-up based on reply quality."""
        task = TASKS[self._current_task_id]
        followups = task.get("followup_messages", {})

        if score < 0.3:
            return followups.get(
                "very_unhappy",
                "This response is completely unhelpful. I need a real solution, not a generic reply!"
            )
        elif score < 0.5:
            return followups.get(
                "unhappy",
                "I appreciate the response, but you haven't actually addressed my issue. "
                "Can you be more specific about what you'll do to help me?"
            )
        else:
            return followups.get(
                "neutral",
                "Thank you for getting back to me. Could you please confirm the specific "
                "next steps and timeline so I know what to expect?"
            )

    def state(self) -> EpisodeState:
        """Return current episode metadata."""
        return EpisodeState(
            step=self._step_count,
            episode_id=self._episode_id,
            task_id=self._current_task_id,
            done=self._done,
            turn_number=self._turn_number,
            cumulative_score=round(self._cumulative_score, 3),
        )
