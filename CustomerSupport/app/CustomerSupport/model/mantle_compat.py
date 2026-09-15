from strands.models.openai_responses import OpenAIResponsesModel


class MantleCompatResponsesModel(OpenAIResponsesModel):
    """Compatibility shim: flattens assistant message content to a plain string.

    Needed because the Bedrock Mantle endpoint (used for gpt-oss-* models) accepts only string
    content, while stock OpenAI also accepts arrays. Not a core lesson concept, just a fix that
    keeps multi-turn conversations working with those models.
    """

    @classmethod
    def _format_request_messages(cls, messages):
        formatted = super()._format_request_messages(messages)
        # Collapse each assistant message's content array into a single string.
        for msg in formatted:
            if msg.get("role") == "assistant" and isinstance(msg.get("content"), list):
                msg["content"] = "".join(
                    part.get("text", "") for part in msg["content"] if part.get("type") == "output_text"
                )
        return formatted
