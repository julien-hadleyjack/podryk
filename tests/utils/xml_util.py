from pydantic_xml import BaseXmlModel


def to_xml(model: BaseXmlModel) -> str:
    return model.to_xml(
        pretty_print=True,
        exclude_none=True,
        skip_empty=True,
        encoding="unicode",
    )
