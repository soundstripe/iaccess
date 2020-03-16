#!/usr/bin/env python

"""Tests for `iaccess` package."""

import pytest
from sqlalchemy.dialects import registry

# noinspection PyUnresolvedReferences
from iaccess.dialect import IAccessDialect

registry.register("iaccess.pyodbc", "iaccess.dialect", "IAccessDialect")

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

# noinspection PyUnresolvedReferences
from sqlalchemy.testing.plugin.pytestplugin import *
