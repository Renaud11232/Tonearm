from dataclasses import dataclass

@dataclass
class VoteStatus:
    required_votes: int
    received_votes: int
    needed_votes: int