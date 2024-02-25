from dataclasses import dataclass
from subprocess import PIPE, Popen
from typing import IO


@dataclass
class MatchResult:
    wins: int
    losses: int
    draws: int
    elo_diff: float


@dataclass
class CutechessMan:
    cutechess: str
    engine: str
    book: str
    games_per: int
    tc: str
    threads: int
    hash: int

    def _get_cutechess_cmd(self, params_a: list[str], params_b: list[str]) -> str:
        return (
            f"{self.cutechess} "
            f"-engine cmd={self.engine} name=params_A proto=uci "
            f"option.Hash={self.hash} {' '.join(params_a)} "
            f"-engine cmd={self.engine} name=params_b proto=uci "
            f"option.Hash={self.hash} {' '.join(params_b)} "
            "-resign movecount=3 score=400 "
            "-draw movenumber=40 movecount=8 score=10 "
            "-repeat "
            "-recover "
            f"-concurrency {self.threads} "
            f"-each tc={self.tc} "
            f"-openings file={self.book} "
            f"format={self.book.split('.')[-1]} order=random plies=16 "
            f"-games {self.games_per} "
            #"-pgnout ./games.pgn"
        )

    def run(self, params_a: list[str], params_b: list[str]) -> MatchResult | None:
        cmd: str = self._get_cutechess_cmd(params_a, params_b)
        cutechess: Popen[bytes] = Popen(cmd.split(), stdout=PIPE)

        score: list[int] = [0, 0, 0]
        elo_diff: float = 0.0
        stdout: IO[bytes] | None = cutechess.stdout

        while stdout is not None:
            # Read each line of output until the pipe closes
            line = stdout.readline().strip().decode("ascii")
            if not line:
                cutechess.wait()
                return MatchResult(score[0], score[1], score[2], elo_diff)
            # Parse WLD score
            if line.startswith("Score of"):
                start_index = line.find(":") + 1
                end_index = line.find("[")
                split = line[start_index:end_index].split(" - ")

                score = [int(i) for i in split]

            # Parse Elo Difference
            if line.startswith("Elo difference"):
                start_index = line.find(":") + 1
                end_index = line.find("+")
                elo_diff = float(line[start_index:end_index])
        return None
