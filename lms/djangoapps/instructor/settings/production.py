"""AWS environment variables unique to the instructor plugin."""
from __future__ import absolute_import

import warnings


def plugin_settings(settings):
    """Settings for the instructor plugin."""
    # Analytics Dashboard
    settings.ANALYTICS_DASHBOARD_URL = settings.ENV_TOKENS.get(
        "ANALYTICS_DASHBOARD_URL", settings.ANALYTICS_DASHBOARD_URL
    )
    settings.ANALYTICS_DASHBOARD_NAME = settings.ENV_TOKENS.get(
        "ANALYTICS_DASHBOARD_NAME", settings.ANALYTICS_DASHBOARD_NAME
    )
    # Backward compatibility for deprecated feature names
    if 'ENABLE_S3_GRADE_DOWNLOADS' in settings.FEATURES:
        warnings.warn(
            "'ENABLE_S3_GRADE_DOWNLOADS' is deprecated. Please use 'ENABLE_GRADE_DOWNLOADS' instead",
            DeprecationWarning,
        )
        settings.FEATURES['ENABLE_GRADE_DOWNLOADS'] = settings.FEATURES['ENABLE_S3_GRADE_DOWNLOADS']
