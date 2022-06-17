"""Bundle of Paper Exporters
"""

from abc import ABC,abstractmethod
from ..models import Paper

class PaperExporter(ABC):
    """Abstract Paper Exporter class"""

    @property
    @abstractmethod
    def format(self) -> str:
        """Export format"""

    @abstractmethod
    def export_paper(self, paper: Paper) -> str:
        """Exports a paper to a readable string

        Args:
            paper (Paper): paper to export

        Returns:
            str: exported version of the paper
        """


class BibTexExporter(PaperExporter):
    """Export that converts Paper into bibtext string"""

    @property
    def format(self) -> str:
        return "bibtex"

    def export_paper(self, paper: Paper) -> str:
        pass

