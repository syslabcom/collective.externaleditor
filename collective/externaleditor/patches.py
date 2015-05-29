from plone.rfc822.interfaces import IPrimaryFieldInfo

FALLBACK_CONTENTTYPE = 'application/octet-stream'


def get_primary_content_type(obj):
    """Get the content type of an item's primary field"""
    primary_field_info = IPrimaryFieldInfo(obj)
    if hasattr(primary_field_info.value, "contentType"):
        contenttype = primary_field_info.value.contentType
    if not contenttype:
        contenttype = FALLBACK_CONTENTTYPE
    return contenttype


def patched_write_metadata(self, RESPONSE, metadata, length):
    parsed_metadata = dict(
        [item.split(':', 1) for item in metadata.splitlines()]
    )
    is_dexterity = parsed_metadata['meta_type'] == 'Dexterity Item'
    if is_dexterity:
        parent = self.aq_parent
        ob = parent[self.REQUEST['target']]
        parsed_metadata['meta_type'] = ob.portal_type
        parsed_metadata['content_type'] = get_primary_content_type(ob)

        metadata = '\n'.join(
            [':'.join(parts) for parts in parsed_metadata.items()])
        clen = RESPONSE.headers.get('content-length', 0)
        length = len(metadata) + int(clen)

    self._old__write_metadata(RESPONSE, metadata, length)
