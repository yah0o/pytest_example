import pytest


def skip_regions_marker(request, config, marker_name, reason=None, include=True):
    marker = request.node.get_closest_marker(marker_name)
    if marker:
        region = config.region
        if not ((region in marker.args) is include):
            pytest.skip('skipped for region: {0}. Reason: {1}'.format(region, reason))
