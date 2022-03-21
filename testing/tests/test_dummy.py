# -*- coding: utf-8 -*-
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import pytest


def sum(num1, num2):
    """It returns sum of two numbers"""
    return num1 + num2

# make sure to start function name with test


@pytest.mark.parametrize('num1, num2, expected',
                         [(3, 5, 8), (-2, -2, -4), (-1, 5, 4), (3, -5, -2), (0, 5, 5)])
def test_sum(num1, num2, expected):
    assert sum(num1, num2) == expected


@pytest.fixture
def get_sum_test_data():
    return [(3, 5, 8), (-2, -2, -4), (-1, 5, 4), (3, -5, -2), (0, 5, 5)]


def test_sum_v2(get_sum_test_data):
    for data in get_sum_test_data:
        num1 = data[0]
        num2 = data[1]
        expected = data[2]
        assert sum(num1, num2) == expected
