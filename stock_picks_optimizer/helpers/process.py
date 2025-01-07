import sys
import time
from signal import SIGINT
from subprocess import Popen, PIPE
from typing import List, AnyStr, IO


class BaseProcessRunner:
    def __init__(self, commands: List[str]) -> None:
        self.__process = Popen(
            commands,
            stdout=PIPE,
            stderr=PIPE,
        )
        time.sleep(3)
        assert not self.__process.poll()

    def read_stdout(self) -> str:
        return self.__read(self.__process.stdout)

    def read_stderr(self) -> str:
        return self.__read(self.__process.stderr)

    def stop(self) -> int:
        self.__process.send_signal(SIGINT)
        self.__process.wait()
        return self.__process.returncode

    def __read(self, reader: IO[AnyStr] | None) -> str:
        if reader is None:
            return ""
        return reader.read().decode("utf-8").strip()  # type: ignore


class PythonModuleRunner(BaseProcessRunner):
    def __init__(self, commands: List[str]) -> None:
        super().__init__([sys.executable, "-m"] + commands)


class StockPicksOptimizerModuleRunner(PythonModuleRunner):
    def __init__(self, commands: List[str]) -> None:
        super().__init__(["stock_picks_optimizer.main"] + commands)
