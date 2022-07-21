from domain import Domain
from signatures.routine.ip_found_but_string_in_body import (
    ip_found_but_string_in_body,
)

from tests import mocks

test = ip_found_but_string_in_body(["::1", "1.1.1.1"], "No domain found here", "INFO")


def test_potential_success_with_matching_ipv4():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1"]
    assert test.potential(domain) == True


def test_potential_success_with_matching_ipv6():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1"]
    assert test.potential(domain) == True


def test_potential_failure_no_matching_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert test.potential(domain) == False


def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_response_with_static_value(
        domain, test.domain_not_configured_message
    )
    assert test.check(domain) == True


def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_response_with_static_value(domain, "Welcome to my site!")
    assert test.check(domain) == False
