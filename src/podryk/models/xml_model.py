from abc import ABC

from pydantic import ConfigDict
from pydantic_xml import BaseXmlModel


class XmlModel(BaseXmlModel, ABC):
    model_config = ConfigDict(
        use_attribute_docstrings=True,
        extra="forbid",
    )
