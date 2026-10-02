"""Short-term memory demo optimized for classroom presentation.

This version allows reusing a pre-provisioned Memory resource to avoid
the 30-120 second wait for resource creation during class.

BEFORE CLASS:
    python classroom-demo.py sdk --setup
    # This creates the memory resource once and saves the ID to memory-id.txt
    # Takes 30-120 seconds, but you only do it once before class starts.

IN CLASS:
    python classroom-demo.py sdk --demo
    # This uses the pre-created resource from memory-id.txt
    # Runs immediately - no wait time!

AFTER CLASS:
    python classroom-demo.py sdk --cleanup
    # This deletes the memory resource to avoid ongoing charges

Prerequisites:
    pip install boto3 bedrock-agentcore
    export AWS_REGION=us-east-1   # use any AgentCore-supported region
"""

import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

REGION = os.getenv("AWS_REGION", "us-east-1")
ACTOR_ID = "user-42"
SESSION_ID = f"sess-{int(time.time())}"
MEMORY_ID_FILE = Path(__file__).parent / "memory-id.txt"


def save_memory_id(memory_id: str) -> None:
    """Save memory ID to file for reuse."""
    MEMORY_ID_FILE.write_text(memory_id)
    print(f"✓ Saved memory ID to {MEMORY_ID_FILE}")


def load_memory_id() -> str:
    """Load memory ID from file."""
    if not MEMORY_ID_FILE.exists():
        print(f"ERROR: {MEMORY_ID_FILE} not found!")
        print("Run with --setup first to create the memory resource.")
        sys.exit(1)
    memory_id = MEMORY_ID_FILE.read_text().strip()
    print(f"✓ Using memory ID from {MEMORY_ID_FILE}: {memory_id}")
    return memory_id


# === Setup: Create and save memory resource (do BEFORE class) ========
def setup_memory() -> None:
    """Create memory resource and save ID for reuse. Run BEFORE class."""
    from bedrock_agentcore.memory import MemoryClient

    print("\n=== SETUP: Creating Memory Resource ===")
    print("This takes 30-120 seconds. You only do this ONCE before class.\n")

    client = MemoryClient(region_name=REGION)
    memory = client.create_memory_and_wait(
        name=f"ClassroomDemo_{int(time.time())}",
        description="Pre-provisioned memory for classroom demo",
        strategies=[],  # No strategies = short-term memory only
        event_expiry_days=30,
    )
    memory_id = memory["id"]
    save_memory_id(memory_id)

    print(f"\n✓ Setup complete! Memory resource created: {memory_id}")
    print(f"✓ You can now run the demo with: python {Path(__file__).name} sdk --demo")


# === Demo: Use pre-created memory (do IN class) ====================
def run_demo() -> None:
    """Run the actual demo using pre-created memory. Fast for IN CLASS use."""
    from bedrock_agentcore.memory import MemorySessionManager
    from bedrock_agentcore.memory.constants import ConversationalMessage, MessageRole

    memory_id = load_memory_id()

    print("\n=== DEMO: Short-Term Memory ===")
    print("Showing: Write conversation turns → Read them back\n")

    # Create a session and add conversation turns
    manager = MemorySessionManager(memory_id=memory_id, region_name=REGION)
    session = manager.create_memory_session(actor_id=ACTOR_ID, session_id=SESSION_ID)

    print("1. Adding conversation turns to memory...")
    session.add_turns(
        messages=[
            ConversationalMessage("Hi, I'm Alex. I prefer Python over Java.", MessageRole.USER),
            ConversationalMessage("Got it, Alex — I'll lean toward Python in examples.", MessageRole.ASSISTANT),
            ConversationalMessage("What did I tell you about my language preference?", MessageRole.USER),
        ]
    )
    print("✓ Added 3 conversation turns")

    # Retrieve conversation turns back
    print("\n2. Retrieving conversation from memory...")
    turns = session.get_last_k_turns(k=5)
    print(f"✓ Retrieved {len(turns)} turns:\n")
    
    for i, turn in enumerate(turns, 1):
        for msg in turn:
            print(f"  Turn {i} - {msg['role']}: {msg['content']['text']}")

    print(f"\n✓ Demo complete! Memory ID: {memory_id}")
    print(f"   (Memory resource is still running - use --cleanup to delete)")


# === Cleanup: Delete memory resource (do AFTER class) ===============
def cleanup_memory() -> None:
    """Delete the memory resource. Run AFTER class to avoid charges."""
    from bedrock_agentcore.memory import MemoryClient

    memory_id = load_memory_id()

    print("\n=== CLEANUP: Deleting Memory Resource ===")
    print(f"Deleting memory: {memory_id}\n")

    client = MemoryClient(region_name=REGION)
    client.delete_memory_and_wait(memory_id=memory_id)

    MEMORY_ID_FILE.unlink()
    print(f"✓ Deleted memory resource: {memory_id}")
    print(f"✓ Removed {MEMORY_ID_FILE}")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mode = args[0] if args else None

    if "--setup" in sys.argv:
        setup_memory()
    elif "--demo" in sys.argv:
        run_demo()
    elif "--cleanup" in sys.argv:
        cleanup_memory()
    else:
        print("Usage:")
        print("  BEFORE CLASS: python classroom-demo.py sdk --setup")
        print("  IN CLASS:     python classroom-demo.py sdk --demo")
        print("  AFTER CLASS:  python classroom-demo.py sdk --cleanup")
        sys.exit(1)


if __name__ == "__main__":
    main()
