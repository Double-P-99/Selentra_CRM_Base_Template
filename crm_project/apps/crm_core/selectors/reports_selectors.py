from apps.crm_core.services.reports_service import CRMReportsService


def get_won_lost_report(*, start_date=None, end_date=None):
    return CRMReportsService.won_lost_report(start_date=start_date, end_date=end_date)


def get_closing_percentage(*, start_date=None, end_date=None):
    return CRMReportsService.closing_percentage_by_executive(start_date=start_date, end_date=end_date)


def get_pipeline_value():
    return CRMReportsService.pipeline_value_by_executive()


def get_monthly_invoicing(*, year=None):
    return CRMReportsService.monthly_invoicing_by_executive(year=year)


def get_average_time_per_stage():
    return CRMReportsService.average_time_per_stage()
