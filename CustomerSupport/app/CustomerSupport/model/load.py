from strands.models.bedrock import BedrockModel


def load_model() -> BedrockModel:
    # Pick which foundation model the agent uses; swap the model_id to try another.
    # Credentials come from the runtime's IAM role, so no keys are needed here.
    return BedrockModel(model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0")
