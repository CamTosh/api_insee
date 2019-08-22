#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import conftest as conf

from api_insee import ApiInsee
from api_insee.conf import API_VERSION
import api_insee.criteria as Criteria

#from api_insee.exeptions.params_exeption import ParamsExeptions

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

api = ApiInsee(
    key = conf.SIRENE_API_CONSUMER_KEY,
    secret = conf.SIRENE_API_CONSUMER_SECRET
)

base_siren_url = API_VERSION['url'] + API_VERSION['path_siren']

def test_siren_search(execute_request):

    request = api.siren('809893225')
    unit    = request.get()

    assert unit['uniteLegale']['siren'] == '809893225'
    assert unit['header']['statut'] == 200
    assert request.url == base_siren_url + '/809893225'

    execute_request(request)

def test_siren_raw_search(execute_request):

    criteria = Criteria.Raw('unitePurgeeUniteLegale:True')
    request  = api.siren(q=criteria)
    results  = request.get()

    assert results['header']['statut'] == 200
    assert request.url == base_siren_url + '?q=unitePurgeeUniteLegale:True'

    execute_request(request)


def test_siren_search_by_field(execute_request):

    criteria = Criteria.Field('unitePurgeeUniteLegale',True)
    request  = api.siren(q=criteria)
    results  = request.get()

    assert results['header']['statut'] == 200
    assert request.url == base_siren_url + '?q=unitePurgeeUniteLegale:True'

    execute_request(request)


def test_siren_search_date(execute_request):

    request = api.siren('005520135', date='2018-01-01')

    assert request.url == base_siren_url + '/005520135?date=2018-01-01'

    execute_request(request)



def test_siren_search_with_period_variable(execute_request):

    request = api.siren(
        q=Criteria.PeriodicField('etatAdministratifUniteLegale','C')
    )

    assert request.url == base_siren_url + '?q=periode(etatAdministratifUniteLegale:C)'

    execute_request(request)


def test_siren_search_exact_field(execute_request):

    request = api.siren(
        q=Criteria.Periodic(Criteria.FieldExact('denominationUniteLegale','LE TIMBRE'))
    )

    assert request.url == base_siren_url + '?q=periode(denominationUniteLegale:"LE TIMBRE")'

    execute_request(request)

