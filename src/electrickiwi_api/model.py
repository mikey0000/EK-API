from typing import List, Optional, Union
from typing import Any

from dataclasses import dataclass
from collections import OrderedDict


@dataclass
class Summary:
    credits: str
    electricity_used: str
    other_charges: str
    payments: str

    @staticmethod
    def from_dict(obj: dict) -> "Summary":
        _credits = str(obj.get("credits"))
        _electricity_used = str(obj.get("electricity_used"))
        _other_charges = str(obj.get("other_charges"))
        _payments = str(obj.get("payments"))
        return Summary(_credits, _electricity_used, _other_charges, _payments)


@dataclass
class AccountBalanceConnection:
    hop_percentage: str
    id: int
    running_balance: str
    start_date: str
    unbilled_days: int

    @staticmethod
    def from_dict(obj: Any) -> "AccountBalanceConnection":
        _hop_percentage = str(obj.get("hop_percentage"))
        _id = int(obj.get("id"))
        _running_balance = str(obj.get("running_balance"))
        _start_date = str(obj.get("start_date"))
        _unbilled_days = int(obj.get("unbilled_days"))
        return AccountBalanceConnection(
            _hop_percentage, _id, _running_balance, _start_date, _unbilled_days
        )



@dataclass
class Connection:
    id: int
    running_balance: str
    unbilled_days: int
    hop_percentage: str
    start_date: str
    service_label: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'Connection':
        return Connection(
            id=int(data.get('id', 0)),
            running_balance=str(data.get('running_balance', '0')),
            unbilled_days=int(data.get('unbilled_days', 0)),
            hop_percentage=str(data.get('hop_percentage', '0')),
            start_date=str(data.get('start_date', '')),
            service_label=str(data.get('service_label', ''))
        )


@dataclass
class ServicePower:
    connections: List[Connection]

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'ServicePower':
        return ServicePower(
            connections=[Connection.from_dict(conn) for conn in data.get('connections', [])]
        )


@dataclass
class AccountSummary:
    type: str
    total_running_balance: str
    total_account_balance: str
    total_billing_days: int
    next_billing_date: str
    service_names: List[str]
    services: dict[str, ServicePower]
    date_to_pay: str
    invoice_id: str
    total_invoiced_charges: str
    default_to_pay: str
    invoice_exists: int
    display_date: str
    last_billed_date: str
    last_billed_amount: str
    summary: Summary
    is_prepay: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'AccountSummary':
        if not data or 'data' not in data:
            raise ValueError("Invalid data format")

        data = data.get('data')
        return AccountSummary(
            type=str(data.get('type', '')),
            total_running_balance=str(data.get('total_running_balance', '0')),
            total_account_balance=str(data.get('total_account_balance', '0')),
            total_billing_days=int(data.get('total_billing_days', 0)),
            next_billing_date=str(data.get('next_billing_date', '')),
            service_names=data.get('service_names', []),
            services={
                'power': ServicePower.from_dict(data.get('services', {}).get('power', {}))
            },
            date_to_pay=str(data.get('date_to_pay', '')),
            invoice_id=str(data.get('invoice_id', '')),
            total_invoiced_charges=str(data.get('total_invoiced_charges', '')),
            default_to_pay=str(data.get('default_to_pay', '')),
            invoice_exists=int(data.get('invoice_exists', 0)),
            display_date=str(data.get('display_date', '')),
            last_billed_date=str(data.get('last_billed_date', '')),
            last_billed_amount=str(data.get('last_billed_amount', '0')),
            summary=Summary.from_dict(data.get('summary', {})),
            is_prepay=str(data.get('is_prepay', ''))
        )

@dataclass
class Customer:
    bill_address_1: str
    bill_address_2: str
    bill_city: str
    bill_company: Union[str, bool]
    bill_name: str
    bill_post_code: str
    billing_day: int
    birth_date: str
    credit_status: str
    customer_status: str
    dummy_schedule_id: int
    email: str
    email_opt_out: str
    external_payment_reference: bool
    first_name: str
    gender: str
    is_active: str
    invite_friend: int
    last_name: str
    mdc: str
    middle_name: str
    phone_area_code: str
    phone_number: str
    retain: str
    signup_date: str
    tcs: str
    update_payment_method: str
    vulnerable_reason: bool
    services: List[str]
    hashKey: str

    @staticmethod
    def from_dict(customer_data: dict) -> "Customer":
        """
        Create a Customer instance from a dictionary.

        Args:
            customer_data: Dictionary containing customer information

        Returns:
            Customer: A new Customer instance
        """
        try:
            customer = customer_data.get("data", {})

            return Customer(
                bill_address_1=str(customer.get("bill_address_1", "")),
                bill_address_2=str(customer.get("bill_address_2", "")),
                bill_city=str(customer.get("bill_city", "")),
                bill_company=customer.get("bill_company", False),
                bill_name=str(customer.get("bill_name", "")),
                bill_post_code=str(customer.get("bill_post_code", "")),
                billing_day=int(customer.get("billing_day", 0)),
                birth_date=str(customer.get("birth_date", "")),
                credit_status=str(customer.get("credit_status", "")),
                customer_status=str(customer.get("customer_status", "")),
                dummy_schedule_id=int(customer.get("dummy_schedule_id", 0)),
                email=str(customer.get("email", "")),
                email_opt_out=str(customer.get("email_opt_out", "")),
                external_payment_reference=bool(customer.get("external_payment_reference", False)),
                first_name=str(customer.get("first_name", "")),
                gender=str(customer.get("gender", "")),
                is_active=str(customer.get("is_active", "")),
                invite_friend=int(customer.get("invite_friend", 0)),
                last_name=str(customer.get("last_name", "")),
                mdc=str(customer.get("mdc", "")),
                middle_name=str(customer.get("middle_name", "")),
                phone_area_code=str(customer.get("phone_area_code", "")),
                phone_number=str(customer.get("phone_number", "")),
                retain=str(customer.get("retain", "")),
                signup_date=str(customer.get("signup_date", "")),
                tcs=str(customer.get("tcs", "")),
                update_payment_method=str(customer.get("update_payment_method", "")),
                vulnerable_reason=bool(customer.get("vulnerable_reason", False)),
                services=customer.get("services", []),
                hashKey=str(customer.get("hashKey", ""))
            )
        except Exception as e:
            raise ValueError(f"Error creating Customer from dictionary: {str(e)}")


@dataclass
class ConnectionHop:
    """Individual Hop start or end on customer connection"""
    start_time: str
    end_time: str
    interval_start: str
    interval_end: str

    @staticmethod
    def from_dict(obj: Any) -> "Hop":
        _start_time = str(obj.get("start_time"))
        _end_time = str(obj.get("end_time"))
        _interval_start = str(obj.get("interval_start"))
        _interval_end = str(obj.get("interval_end"))
        return ConnectionHop(_start_time, _end_time, _interval_start, _interval_end)


@dataclass
class CustomerConnection:
    type: str
    id: int
    customer_number: int
    identifier: str
    address: str
    is_active: str
    hop: ConnectionHop
    start_date: str
    end_date: str

    @staticmethod
    def from_dict(customer_connection_data: Any) -> "CustomerConnection":
        customer_connection = customer_connection_data.get("data")

        _type = str(customer_connection.get("type"))
        _id = int(customer_connection.get("id"))
        _customer_number = int(customer_connection.get("customer_number"))
        _identifier = str(customer_connection.get("identifier"))
        _address = str(customer_connection.get("address"))
        _is_active = str(customer_connection.get("is_active"))
        _hop = ConnectionHop.from_dict(customer_connection.get("hop"))
        _start_date = str(customer_connection.get("start_date"))
        _end_date = str(customer_connection.get("end_date"))
        return CustomerConnection(
            _type,
            _id,
            _customer_number,
            _identifier,
            _address,
            _is_active,
            _hop,
            _start_date,
            _end_date,
        )


@dataclass
class BillingAddress:
    bill_address_1: str
    bill_address_2: str
    bill_city: str
    bill_company: str
    bill_name: str
    bill_post_code: str
    type: str
    id: int

    @staticmethod
    def from_dict(billing_address_data: dict) -> "BillingAddress":
        billing_address = billing_address_data.get("data")

        _id = str(billing_address.get("id"))
        _address_1 = str(billing_address.get("bill_address_1"))
        _address_2 = str(billing_address.get("bill_address_2"))
        _city = str(billing_address.get("bill_city"))
        _company = str(billing_address.get("bill_company"))
        _name = str(billing_address.get("bill_name"))
        _post_code = str(billing_address.get("bill_post_code"))
        _type = str(billing_address.get("type"))
        return BillingAddress(
            _address_1, _address_2, _city, _company, _name, _post_code, _type
        )


@dataclass
class BillingFrequency:
    billing_date: str
    day: str
    frequency: str
    period: str
    type: str

    @staticmethod
    def from_dict(billing_frequency_data: dict) -> "BillingFrequency":
        billing_frequency = billing_frequency_data.get("data")
        _billing_date = str(billing_frequency.get("billing_date"))
        _day = str(billing_frequency.get("day"))
        _frequency = str(billing_frequency.get("frequency"))
        _period = str(billing_frequency.get("period"))
        _type = str(billing_frequency.get("type"))
        return BillingFrequency(_billing_date, _day, _frequency, _period, _type)


@dataclass
class Bill:
    date_to_pay: str
    date_generated: str
    end_date: str
    file: str
    id: int
    invoice_total_charges_incl_gst: float
    start_date: str
    status: str
    status_message: str
    title: str
    total_to_pay: float
    type: str

    @staticmethod
    def from_dict(bill_data: Any) -> "Bill":
        bill = bill_data.get("data")
        if bill is None:
            bill = bill_data

        _date_to_pay = str(bill.get("date_to_pay"))
        _date_generated = str(bill.get("date_generated"))
        _end_date = str(bill.get("end_date"))
        _file = str(bill.get("file"))
        _id = int(bill.get("id"))
        _invoice_total_charges_incl_gst = float(
            bill.get("invoice_total_charges_incl_gst")
        )
        _start_date = str(bill.get("start_date"))
        _status = str(bill.get("status"))
        _status_message = str(bill.get("status_message"))
        _title = str(bill.get("title"))
        _total_to_pay = float(bill.get("total_to_pay"))
        _type = str(bill.get("type"))
        return Bill(
            _date_to_pay,
            _date_generated,
            _end_date,
            _file,
            _id,
            _invoice_total_charges_incl_gst,
            _start_date,
            _status,
            _status_message,
            _title,
            _total_to_pay,
            _type,
        )


@dataclass
class Links:
    first: str
    last: str
    next: str
    previous: str
    self: str

    @staticmethod
    def from_dict(obj: Any) -> "Links":
        _first = str(obj.get("first"))
        _last = str(obj.get("last"))
        _next = str(obj.get("next"))
        _previous = str(obj.get("previous"))
        _self = str(obj.get("self"))
        return Links(_first, _last, _next, _previous, _self)


@dataclass
class Pagination:
    limit: int
    links: Links
    offset: int
    page_count: int
    total_count: int

    @staticmethod
    def from_dict(obj: Any) -> "Pagination":
        _limit = int(obj.get("limit"))
        _links = Links.from_dict(obj.get("links"))
        _offset = int(obj.get("offset"))
        _page_count = int(obj.get("page_count"))
        _total_count = int(obj.get("total_count"))
        return Pagination(_limit, _links, _offset, _page_count, _total_count)


@dataclass
class Meta:
    pagination: Pagination

    @staticmethod
    def from_dict(obj: Any) -> "Meta":
        _pagination = Pagination.from_dict(obj.get("pagination"))
        return Meta(_pagination)


@dataclass
class Bills:
    bills: List[Bill]
    meta: Meta
    type: str

    @staticmethod
    def from_dict(bills_data: dict) -> "Bills":
        bills = bills_data.get("data")

        _bills = [Bill.from_dict(y) for y in bills.get("bills")]
        _meta = Meta.from_dict(bills.get("meta"))
        _type = str(bills.get("type"))
        return Bills(_bills, _meta, _type)


@dataclass
class BillFile:
    file_base64: str
    file_name: str
    id: int
    type: str

    @staticmethod
    def from_dict(bill_file_data: dict) -> "BillFile":
        bill_file = bill_file_data.get("data")
        _file_base64 = str(bill_file.get("file_base64"))
        _file_name = str(bill_file.get("file_name"))
        _id = int(bill_file.get("id"))
        _type = str(bill_file.get("type"))
        return BillFile(_file_base64, _file_name, _id, _type)


@dataclass
class ConsumptionRange:
    end_date: str
    start_date: str

    @staticmethod
    def from_dict(obj: Any) -> "ConsumptionRange":
        _end_date = str(obj.get("end_date"))
        _start_date = str(obj.get("start_date"))
        return ConsumptionRange(_end_date, _start_date)


@dataclass
class UsageCharge:
    end_date: str
    fixed_rate_incl_gst: str
    hop_saving: str
    start_date: str
    supply_days: int
    total_consumption: str
    total_fixed_charges_incl_gst: str
    total_variable_charges_incl_gst: str
    variable_rate_incl_gst: str

    @staticmethod
    def from_dict(obj: Any) -> "UsageCharge":
        _end_date = str(obj.get("end_date"))
        _fixed_rate_incl_gst = str(obj.get("fixed_rate_incl_gst"))
        _hop_saving = str(obj.get("hop_saving"))
        _start_date = str(obj.get("start_date"))
        _supply_days = int(obj.get("supply_days"))
        _total_consumption = str(obj.get("total_consumption"))
        _total_fixed_charges_incl_gst = str(obj.get("total_fixed_charges_incl_gst"))
        _total_variable_charges_incl_gst = str(
            obj.get("total_variable_charges_incl_gst")
        )
        _variable_rate_incl_gst = str(obj.get("variable_rate_incl_gst"))
        return UsageCharge(
            _end_date,
            _fixed_rate_incl_gst,
            _hop_saving,
            _start_date,
            _supply_days,
            _total_consumption,
            _total_fixed_charges_incl_gst,
            _total_variable_charges_incl_gst,
            _variable_rate_incl_gst,
        )


@dataclass
class ConsumptionSummary:
    range: ConsumptionRange
    usage: List[UsageCharge]
    type: str

    @staticmethod
    def from_dict(consumption_summary_data: Any) -> "ConsumptionSummary":
        consumption_summary = consumption_summary_data.get("data")
        _range = ConsumptionRange.from_dict(consumption_summary.get("range"))
        _usage_charges = [
            UsageCharge.from_dict(y) for y in consumption_summary.get("usage")
        ]
        _type = str(consumption_summary.get("type"))
        return ConsumptionSummary(_range, _usage_charges, _type)


# HOP


@dataclass
class Interval:
    consumption: str
    hop_best: int
    time: str

    @staticmethod
    def from_dict(obj: Any) -> "Interval":
        _consumption = str(obj.get("consumption"))
        _hop_best = int(obj.get("hop_best"))
        _time = str(obj.get("time"))
        return Interval(_consumption, _hop_best, _time)


@dataclass
class UsageRange:
    end_date: str
    start_date: str
    group_by: str

    @staticmethod
    def from_dict(obj: Any) -> "UsageRange":
        _end_date = str(obj.get("end_date"))
        _start_date = str(obj.get("start_date"))
        _group_by = str(obj.get("group_by"))
        return UsageRange(_end_date, _start_date, _group_by)


@dataclass
class Usage:
    adjustment_charges_incl_gst: str
    bill_consumption: str
    consumption: str
    consumption_adjustment: str
    fixed_charges_excl_gst: str
    fixed_charges_incl_gst: str
    intervals: List[dict]
    percent_consumption_adjustment: str
    range: UsageRange
    status: str
    total_charges_incl_gst: str
    type: str
    variable_charges_excl_gst: str
    variable_charges_incl_gst: str

    @staticmethod
    def from_dict(usage: dict) -> "Usage":
        _adjustment_charges_incl_gst = str(usage.get("adjustment_charges_incl_gst"))
        _bill_consumption = str(usage.get("bill_consumption"))
        _consumption = str(usage.get("consumption"))
        _consumption_adjustment = str(usage.get("consumption_adjustment"))
        _fixed_charges_excl_gst = str(usage.get("fixed_charges_excl_gst"))
        _fixed_charges_incl_gst = str(usage.get("fixed_charges_incl_gst"))
        _intervals = [
            {y: [Usage.from_dict(usage.get("intervals").get(y))]}
            for y in usage.get("usage").keys()
        ]
        _percent_consumption_adjustment = str(
            usage.get("percent_consumption_adjustment")
        )
        _range = UsageRange.from_dict(usage.get("range"))
        _status = str(usage.get("status"))
        _total_charges_incl_gst = str(usage.get("total_charges_incl_gst"))
        _type = str(usage.get("type"))
        _variable_charges_excl_gst = str(usage.get("variable_charges_excl_gst"))
        _variable_charges_incl_gst = str(usage.get("variable_charges_incl_gst"))
        return Usage(
            _adjustment_charges_incl_gst,
            _bill_consumption,
            _consumption,
            _consumption_adjustment,
            _fixed_charges_excl_gst,
            _fixed_charges_incl_gst,
            _intervals,
            _percent_consumption_adjustment,
            _range,
            _status,
            _total_charges_incl_gst,
            _type,
            _variable_charges_excl_gst,
            _variable_charges_incl_gst,
        )


@dataclass
class ConsumptionAverage:
    group_breakdown: List[str]
    range: ConsumptionRange
    type: str
    usage: List[dict]

    @staticmethod
    def from_dict(consumption_average_data: dict) -> "ConsumptionAverage":
        consumption_average = consumption_average_data.get("data")
        _group_breakdown = consumption_average.get("group_breakdown")
        _range = ConsumptionRange.from_dict(consumption_average.get("range"))
        _type = str(consumption_average.get("type"))
        _usage = [
            {y: [Usage.from_dict(consumption_average.get("usage").get(y))]}
            for y in consumption_average.get("usage").keys()
        ]
        return ConsumptionAverage(_group_breakdown, _range, _type, _usage)


@dataclass
class HopInterval:
    active: int
    end_time: str
    start_time: str

    @staticmethod
    def from_dict(obj: Any) -> "HopInterval":
        _active = int(obj.get("active"))
        _end_time = str(obj.get("end_time"))
        _start_time = str(obj.get("start_time"))
        return HopInterval(_active, _end_time, _start_time)


@dataclass
class HopIntervals:
    type: str
    hop_duration: str
    intervals: OrderedDict[int, HopInterval]
    service_type: str

    @staticmethod
    def from_dict(hop_intervals_data: Any) -> "HopIntervals":
        hop_intervals = hop_intervals_data.get("data")
        _hop_duration = str(hop_intervals.get("hop_duration"))
        _type = str(hop_intervals.get("type"))
        _intervals = OrderedDict()
        for y in hop_intervals.get("intervals").keys():
            _intervals[int(y)] = HopInterval.from_dict(
                hop_intervals.get("intervals").get(y)
            )
        _intervals = OrderedDict(sorted(_intervals.items()))
        _service_type = hop_intervals.get("service_type")
        return HopIntervals(_hop_duration, _type, _intervals, _service_type)


@dataclass
class End:
    end_time: str
    interval: str

    @staticmethod
    def from_dict(obj: Any) -> "End":
        _end_time = str(obj.get("end_time"))
        _interval = str(obj.get("interval"))
        return End(_end_time, _interval)


@dataclass
class Start:
    start_time: str
    interval: str

    @staticmethod
    def from_dict(obj: Any) -> "Start":
        _start_time = str(obj.get("start_time"))
        _interval = str(obj.get("interval"))
        return Start(_start_time, _interval)


@dataclass
class Hop:
    connection_id: str
    customer_number: int
    end: End
    start: Start
    type: str
    service_type: str

    @staticmethod
    def from_dict(hop_data: Any) -> "Hop":
        hop = hop_data.get("data")
        _connection_id = str(hop.get("connection_id"))
        _customer_number = int(hop.get("customer_id"))
        _end = End.from_dict(hop.get("end"))
        _start = Start.from_dict(hop.get("start"))
        _type = str(hop.get("type"))
        _service_type = str(hop.get("service_type"))
        return Hop(_connection_id, _customer_number, _end, _start, _type, _service_type)


@dataclass
class Subscriptions:
    bill_alert: str
    stay_ahead: str

    @staticmethod
    def from_dict(obj: Any) -> "Subscriptions":
        _bill_alert = str(obj.get("bill_alert"))
        _stay_ahead = str(obj.get("stay_ahead"))
        return Subscriptions(_bill_alert, _stay_ahead)


@dataclass
class Service:
    service: str
    identifier: str
    is_primary_service: bool
    service_status: str

    @staticmethod
    def from_dict(service: Any) -> "Service":
        return Service(
            service=str(service.get("service")),
            identifier=str(service.get("identifier")),
            is_primary_service=bool(service.get("is_primary_service")),
            service_status=str(service.get("service_status"))
        )


@dataclass
class SessionCustomer:
    customer_number: int
    customer_name: str
    email: str
    customer_status: str
    services: List[Service]
    res_partner_id: int
    nuid: str
    avatar: List  # Keeping as List since it's empty in the example

    def get_primary_electricity_service(self) -> Optional[Service]:
        """Get the primary electricity service if it exists."""
        for service in self.services:
            if (service.service.lower() == "electricity"
                    and service.is_primary_service):
                return service
        return None

    @staticmethod
    def from_dict(customer: Any) -> "SessionCustomer":
        return SessionCustomer(
            customer_number=int(customer.get("customer_number")),
            customer_name=str(customer.get("customer_name")),
            email=str(customer.get("email")),
            customer_status=str(customer.get("customer_status")),
            services=[Service.from_dict(service) for service in customer.get("services", [])],
            res_partner_id=int(customer.get("res_partner_id")),
            nuid=str(customer.get("nuid")),
            avatar=customer.get("avatar", [])
        )


@dataclass
class Session:
    data: SessionCustomer
    status: int

    @staticmethod
    def from_dict(session_data: Any) -> "Session":
        if data := session_data.get("data"):
            if session := data.get("data"):
                return Session(
                    data=SessionCustomer.from_dict(session),
                    status=int(session_data.get("status", 0))
                )
        return Session(None, 0)  # Or handle this case as needed


@dataclass
class OutageContact:
    message: str
    network_name: str
    outage_url: str
    phone_number: str
    type: str

    @staticmethod
    def from_dict(outage_contact_data: Any) -> "OutageContact":
        outage_contact = outage_contact_data.get("data")
        _message = str(outage_contact.get("message"))
        _network_name = str(outage_contact.get("network_name"))
        _outage_url = str(outage_contact.get("outage_url"))
        _phone_number = str(outage_contact.get("phone_number"))
        _type = str(outage_contact.get("type"))
        return OutageContact(_message, _network_name, _outage_url, _phone_number, _type)
