from abc import ABC, abstractmethod

from app.core.artifact import ResearchArtifact


class BaseAgent(ABC):
    """
    Base class for all AI agents.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def analyze(self, artifact: ResearchArtifact) -> ResearchArtifact:
        ...