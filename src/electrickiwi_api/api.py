from typing import Any

from electrickiwi_api.auth import AbstractAuth
from electrickiwi_api.exceptions import AuthException, ApiException
from electrickiwi_api.model import Hop, HopIntervals, BillFile, \
    Bills, BillingFrequency, BillingAddress, CustomerConnection, Customer, Session, AccountSummary, Service, ConsumptionAverage



class ElectricKiwiEndpoint:
    # scope read_customer_detail
    customer = "/user/details/v1/{customerNumber}"
    # user services
    user_services = "/user/services/v1/{customerNumber}"
    # scope read_connection_detail
    customer_connection_details = "/power/v1/connection/details/{customerNumber}/{identifier}/"
    billing_details = "/user/v1/billing/details/{customerNumber}"
    # scope read_billing_address
    billing_address = "/user/v1/billing/address/{customerNumber}/"
    # scope read_billing_frequency
    billing_frequency = "/user/v1/billing/frequency/{customerNumber}/"
    # scope read_billing_bills
    billing_bills = "/user/v1/billing/bills/{customerNumber}/?limit={limit}&offset={offset}/"
    # scope read_billing_bill_file
    billing_bill_file = "/user/v1/billing/invoice/{customerNumber}/{billId}/"
    # scope read_account_running_balance
    account_summary = "/user/account/v1/summary/{customerNumber}/"
    # scope read_consumption_averages
    consumption_insights = "/power/usage/v1/insights/{customerNumber}/{identifier}/?start_date={startDate}&end_date={" \
                          "endDate}&group_by={groupBy} "
    # scope read_hop_intervals_config
    hourofpower_intervals = "/power/products/v1/hop_intervals"
    # scope read_hop_connection, save_hop_connection (POST) (hour of power)
    hourofpower_by_connection = "/power/products/v1/hop/{customerNumber}/{identifier}/"
    # scope read_outage_contact
    # outageContactInformationForConnection = "/service/outage/contact/{identifier}/"
    # read_session
    session = "/user/v5/session"


def get_next_page(response) -> dict[str, Any]:
    return {
        "limit": response["meta"]["pagination"]["limit"],
        "offset": response["meta"]["pagination"]["offset"] + response["meta"]["pagination"]["limit"],
    }


def check_status(status):
    if status == 401:
        raise AuthException(f"Authorization failed: {status}")
    if status != 200:
        raise ApiException(f"Error request failed: {status}")


class ElectricKiwiApi:
    """Electric Kiwi API"""

    def __init__(self, auth: AbstractAuth) -> None:
        self.customer_number: int = None
        self.session: Session = None
        self.electricity: Service = None
        self.auth = auth

    async def set_active_session(self) -> None:
        resp = await self.auth.request("get", ElectricKiwiEndpoint.session)
        check_status(resp.status)

        session = Session.from_dict(await resp.json())
        self.customer_number = session.data.customer_number
        self.session = session
        self.electricity = self.session.data.get_primary_electricity_service()
        if self.electricity is None:
            raise ApiException(f"Electricity service not found")

    async def get_active_session(self) -> Session:
        session = await self.auth.request("get", ElectricKiwiEndpoint.session)
        check_status(session.status)
        return Session.from_dict(await session.json())

    async def get_customer(self) -> Customer:
        customer = await self.auth.request("get",
                                           ElectricKiwiEndpoint.customer.format(customerNumber=self.customer_number))
        check_status(customer.status)
        return Customer.from_dict(await customer.json())

    async def get_connection_details(self) -> CustomerConnection:
        connection_details = await self.auth.request("get", ElectricKiwiEndpoint.customer_connection_details.format(
            customerNumber=self.customer_number,
            identifier=self.electricity.identifier))
        check_status(connection_details.status)
        return CustomerConnection.from_dict(await connection_details.json())

    async def get_billing_address(self) -> BillingAddress:
        billing_address = await self.auth.request("get",
                                                  ElectricKiwiEndpoint.billing_address.format(
                                                      customerNumber=self.customer_number))
        check_status(billing_address.status)
        return BillingAddress.from_dict(await billing_address.json())

    async def get_billing_frequency(self) -> BillingFrequency:
        billing_frequency = await self.auth.request("get", ElectricKiwiEndpoint.billing_frequency.format(
            customerNumber=self.customer_number))
        check_status(billing_frequency.status)
        return BillingFrequency.from_dict(await billing_frequency.json())

    #@paginated(by_query_params=get_next_page)
    async def get_billing_bills(self, limit = 5, offset = 0) -> Bills:
        billing_bills = await self.auth.request("get", ElectricKiwiEndpoint.billing_bills.format(customerNumber=self.customer_number, limit=limit, offset=offset))
        check_status(billing_bills.status)
        return Bills.from_dict(await billing_bills.json())

    async def get_bill_file(self, bill_id) -> BillFile:
        bill_file = await self.auth.request("get",
                                            ElectricKiwiEndpoint.billing_bill_file.format(
                                                customerNumber=self.customer_number,
                                                billId=bill_id))
        check_status(bill_file.status)
        return BillFile.from_dict(await bill_file.json())

    async def get_account_summary(self) -> AccountSummary:
        account_summary = await self.auth.request("get",
                                                  ElectricKiwiEndpoint.account_summary.format(
                                                      customerNumber=self.customer_number))
        check_status(account_summary.status)
        return AccountSummary.from_dict(await account_summary.json())


    async def get_consumption_averages(self, start_date, end_date, group_by="week") -> ConsumptionAverage:
        consumption_average = await self.auth.request("get", ElectricKiwiEndpoint.consumption_insights.format(
            customerNumber=self.customer_number,
            identifier=self.electricity.identifier),
                                                      json={start_date: start_date, end_date: end_date,
                                                            group_by: group_by})
        check_status(consumption_average.status)
        return ConsumptionAverage.from_dict(await consumption_average.json())

    async def get_hop_intervals(self) -> HopIntervals:
        hop_intervals = await self.auth.request("get", ElectricKiwiEndpoint.hourofpower_intervals)
        check_status(hop_intervals.status)
        return HopIntervals.from_dict(await hop_intervals.json())

    async def get_hop(self) -> Hop:
        get_hop = await self.auth.request("get", ElectricKiwiEndpoint.hourofpower_by_connection.format(
            customerNumber=self.customer_number,
            identifier=self.electricity.identifier))
        check_status(get_hop.status)
        return Hop.from_dict(await get_hop.json())

    async def post_hop(self, hop_interval: int) -> Hop:
        data = {id: str(self.customer_number), "start": hop_interval}
        post_hop = await self.auth.request("post", ElectricKiwiEndpoint.hourofpower_by_connection.format(
            customerNumber=self.customer_number,
            identifier=self.electricity.identifier),
                                           json=data)
        check_status(post_hop.status)
        return Hop.from_dict(await post_hop.json())
