import uuid

from syrupy import SnapshotAssertion

from podryk.models.episode import Guid

from .utils.xml_util import to_xml


# noinspection PyMethodMayBeStatic
class TestGuid:
    def test_full_url_permalink_default(self, snapshot: SnapshotAssertion):
        guid = Guid(guid="https://example.com")
        assert guid.is_permalink is None
        assert to_xml(guid) == snapshot

    def test_uuid_permalink_default(self, snapshot: SnapshotAssertion):
        guid = Guid(guid=uuid.UUID('{12345678-1234-5678-1234-567812345678}'))
        assert guid.is_permalink is False
        assert to_xml(guid) == snapshot

    def test_uuid_force_permalink(self, snapshot: SnapshotAssertion):
        guid = Guid(guid=uuid.UUID('{12345678-1234-5678-1234-567812345678}'), is_permalink=True)
        assert to_xml(guid) == snapshot