#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import numpy as np

import cyphi


def test_null_concept(s):
    assert (s.null_concept() == cyphi.models.Concept(
        mechanism=(),
        location=np.array([s.unconstrained_cause_repertoire(s.nodes),
                           s.unconstrained_effect_repertoire(s.nodes)]),
        phi=0, cause=None, effect=None))


def test_concept_nonexistent(s):
    assert not s.concept((s.nodes[0], s.nodes[2]))


# TODO finish
def test_concept(s):
    pass


def big_phi_standard_example(subsystem):
    initial_precision = cyphi.constants.PRECISION
    cyphi.constants.PRECISION = 4
    assert cyphi.utils.phi_eq(cyphi.compute.big_phi(subsystem), 2.3125)
    cyphi.constants.PRECISION = initial_precision


def test_big_phi_standard_example_sequential(s):
    initial = cyphi.options.PARALLEL_CUT_EVALUATION
    cyphi.options.PARALLEL_CUT_EVALUATION = False
    big_phi_standard_example(s)
    cyphi.options.PARALLEL_CUT_EVALUATION = initial


def test_big_phi_standard_example_parallel(s):
    initial = cyphi.options.PARALLEL_CUT_EVALUATION
    cyphi.options.PARALLEL_CUT_EVALUATION = True
    big_phi_standard_example(s)
    cyphi.options.PARALLEL_CUT_EVALUATION = initial


@pytest.mark.slow
def test_big_mip_big_network(big_subsys_all):
    initial_precision = cyphi.constants.PRECISION
    cyphi.constants.PRECISION = 4
    mip = cyphi.compute.big_mip(big_subsys_all)
    assert cyphi.utils.phi_eq(mip.phi, 10.744578)
    assert cyphi.utils.phi_eq(
        sum(C.phi for C in mip.unpartitioned_constellation),
        6.464257107140015)
    assert cyphi.utils.phi_eq(
        sum(c.phi for c in mip.partitioned_constellation),
        3.564907)
    assert len(mip.unpartitioned_constellation) == 30
    assert len(mip.partitioned_constellation) == 17
    cyphi.constants.PRECISION = initial_precision
