
import boto3
import datetime

from math import sqrt


import logging
from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.note
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# get_cost_and_usage parameters
GRANULARITY = 'DAILY'  # 'DAILY'|'MONTHLY'|'HOURLY'
DIMENSION_KEY = 'SERVICE'  # 'AZ'|'INSTANCE_TYPE'|'LINKED_ACCOUNT'|'OPERATION'|'PURCHASE_TYPE'|'REGION'|'SERVICE'|'USAGE_TYPE'|'USAGE_TYPE_GROUP'|'RECORD_TYPE'|'OPERATING_SYSTEM'|'TENANCY'|'SCOPE'|'PLATFORM'|'SUBSCRIPTION_ID'|'LEGAL_ENTITY_NAME'|'DEPLOYMENT_OPTION'|'DATABASE_ENGINE'|'CACHE_ENGINE'|'INSTANCE_TYPE_FAMILY'|'BILLING_ENTITY'|'RESERVATION_ID'|'RESOURCE_ID'|'RIGHTSIZING_TYPE'|'SAVINGS_PLANS_TYPE'|'SAVINGS_PLAN_ARN'|'PAYMENT_OPTION'
GROUP_BY_TYPE = 'DIMENSION'  # 'DIMENSION'|'TAG'|'COST_CATEGORY'
GROUP_BY_KEY = 'USAGE_TYPE'  # 'AZ'|'INSTANCE_TYPE'|'LEGAL_ENTITY_NAME'|'LINKED_ACCOUNT'|'OPERATION'|'PLATFORM'|'PURCHASE_TYPE'|'SERVICE'|'TAGS'|'TENANCY'|'RECORD_TYPE'|'USAGE_TYPE'
METRIC = "UnblendedCost"  # 'AmortizedCost'|'BlendedCost'|'NetAmortizedCost'|'NetUnblendedCost'|'UnblendedCost'

# get cost explorer client
client = boto3.client('ce')

arcimoto.args.register({
    'threshold': {
        'type': 'number',
        'default': 3,
        'min': 1
    },
    'num_days': {
        'type': 'number',
        'default': 20,
        'min': 2
    }
})

@arcimoto.runtime.handler
def utility_notify_aws_cost_and_usage_daily(threshold, num_days):

  return daily_aws_cost_and_usage(num_days_to_check=num_days, sigma_alarm_threshold=threshold)

def get_avg_and_stddev(cost_list):
    """
    cost_list must have at least 2 elements
    """
    # average
    n_costs = len(cost_list)
    cost_sum = sum(cost_list)
    average = cost_sum / n_costs

    # standard_deviation
    partial_variance = 0
    for cost in cost_list:
        partial_variance += (cost - average)**2
    stddev = sqrt(partial_variance / (n_costs - 1))

    return average, stddev


def get_service_names(start_day, end_day):
    try:
        response = client.get_dimension_values(Dimension='SERVICE', TimePeriod={'Start': start_day, 'End': end_day})
    except Exception as e:
        logger.error(f"Exception in Cost Explorer\'s get_service_names: {e}")
    name_list = []
    for dimension in response['DimensionValues']:
        name_list.append(dimension['Value'])

    return name_list


def get_date_range(num_days_to_check):
    # get dates
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    start_day = today - datetime.timedelta(days=num_days_to_check + 1)
    end_day = today  # + datetime.timedelta(days=1)
    # get iso format dates
    today_date = today.isoformat()
    yesterday_date = yesterday.isoformat()
    start_date_inclusive = start_day.isoformat()
    end_date_exclusive = end_day.isoformat()
    # get posix format dates
    # today_date_posix = int(time.mktime(today.timetuple()))
    # yesterday_date_posix = int(time.mktime(yesterday.timetuple()))
    # start_date_posix = int(time.mktime(start_day.timetuple()))
    # end_date_posix = int(time.mktime(end_day.timetuple()))

    return start_date_inclusive, yesterday_date, end_date_exclusive


def get_cost_lists(num_days_to_check):
    """
    Purpose:
        Get the lists of costs from AWS
    Inputs:
        num_days_to_check: the number of days prior to today to use for determining avg, stddev.
            must be 2 or more
    Returns:
        cost_lists: a dictionary of costs prior to today; keys are cost categories, values are lists of costs
        yesterday_costs: a dictionary of costs: keys are cost categories, value is yesterday's cost
    """
    # get dates
    start_date_inclusive, yesterday_date, end_date_exclusive = get_date_range(num_days_to_check)

    # get list of service names for time period
    service_list = get_service_names(start_date_inclusive, end_date_exclusive)

    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date_inclusive,
                'End': end_date_exclusive
            },
            Granularity=GRANULARITY,
            Filter={
                "Dimensions": {
                    "Key": DIMENSION_KEY,
                    "Values": service_list
                }
            },
            Metrics=[
                METRIC
            ],
            GroupBy=[
                {
                    'Type': GROUP_BY_TYPE,
                    'Key': GROUP_BY_KEY
                },
            ]
        )
    except Exception as e:
        logger.error(f"Exception in Cost Explorer\'s get_cost_and_usage: {e}")
        raise ArcimotoAlertException(f"Exception in Cost Explorer\'s get_cost_and_usage: {e}")

    # create dictionary with cost keys as dictionary keys
    cost_lists = {}
    for day_num in range(num_days_to_check + 1):
        groups = response['ResultsByTime'][day_num]['Groups']
        for group in groups:
            key = group['Keys'][0]
            if key not in cost_lists:
                cost_lists[key] = []

    # reform response into arrays
    yesterday_costs = {}  # key is cost category, value is cost
    for day_num in range(num_days_to_check + 1):
        day = response['ResultsByTime'][day_num]['TimePeriod']['Start']
        groups = response['ResultsByTime'][day_num]['Groups']
        for group in groups:
            key = group['Keys'][0]
            metric_cost = group['Metrics'][METRIC]
            amount = metric_cost['Amount']
            unit = metric_cost['Unit']
            if unit != 'USD':
                logger.warning(f"Warning: cost unit for {key} is not USD: {unit}")

            # append to today_costs xor cost_lists
            if day == yesterday_date:
                yesterday_costs[key] = float(amount)
            else:
                cost_lists[key].append(float(amount))

    return cost_lists, yesterday_costs


def get_cost_center_tag(usage_type, start_date, end_date):
    """
    Purpose:
        Build a markdown tag containing a url for the AWS Cost Management Cost Explorer Console for usage_type from start_date to end_date
    Returns:
        a string containing a url
    """
    url_string = "https://console.aws.amazon.com/cost-reports/home?region=us-west-2#/custom?groupBy=TagKeyValue:Cost%20Center&hasBlended=false&hasAmortized=false&excludeDiscounts=true&excludeTaggedResources=false&excludeCategorizedResources=false&timeRangeOption=Custom&granularity=Daily&reportName=&reportType=CostUsage&isTemplate=true&startDate=replace_string_start_date&endDate=replace_string_end_date&filter=%5B%7B%22dimension%22:%22UsageType%22,%22values%22:%5B%7B%22value%22:%22replace_string_usage_type%22,%22unit%22:%22GB%22%7D%5D,%22include%22:true,%22children%22:null%7D%5D&forecastTimeRangeOption=None&usageAs=usageQuantity&chartStyle=Stack&excludeForecast=true"
    url_string = url_string.replace("replace_string_usage_type", usage_type)
    url_string = url_string.replace("replace_string_start_date", start_date)
    url_string = url_string.replace("replace_string_end_date", end_date)

    return "<{}|Cost Explorer: Cost & Usage>".format(url_string)


def daily_aws_cost_and_usage(num_days_to_check=20, sigma_alarm_threshold=3):
    """
    Purpose:
        Monitor AWS costs based on categories.  This function breaks down usage by a combination of SERVICE and USAGE_TYPE.
        A specified number (num_days_to_check) of days prior to the most recently completed day are used to find an average
        and standard deviation of each SERVICE/USAGE_TYPE cost.  If the most recently completed day's cost exceeds the
        average by a specified number (sigma_alarm_threshold) of standard deviations, an alarm is raised.
    Inputs:
        num_days_to_check: the number of days prior to today to use for determining avg, stddev.
            must be 2 or more
        sigma_alarm_threshold:  the number of standard deviations by which a metric must vary in order to trip an alarm
    """
    # get cost lists
    cost_lists, yesterday_costs = get_cost_lists(num_days_to_check)

    costs_over_threshold = {}
    for key, cost_list in cost_lists.items():
        if key in yesterday_costs:
            # define upper and lower alarm thresholds
            average, stddev = get_avg_and_stddev(cost_list)
            upper = average + stddev * sigma_alarm_threshold
            lower = average - stddev * sigma_alarm_threshold

            # check for excessive deviation from average
            cost = yesterday_costs[key]
            if cost > upper:
                costs_over_threshold[key] = {
                    "cost": cost,
                    "lower": lower,
                    "upper": upper
                }
            if cost > upper or cost < lower:
                logger.info(f" cost outside threshold! lower: {lower}, upper: {upper}, cost: {cost}")

        else:
            logger.info(f"cost {key} does not exist today.")

    logger.info(f"Costs over threshsold: {costs_over_threshold}")

    # get dates
    start_date, yesterday_date, end_date = get_date_range(num_days_to_check)

    # Send notification for each overage
    for usage_type, cost_values in costs_over_threshold.items():
        url_string = get_cost_center_tag(usage_type, start_date, yesterday_date)
        # msg = "Daily AWS cost for `{}` is over the expected range (between {:.2e} and {:.2e} USD) at {:.2e} USD.\n".format(usage_type, cost_values["lower"], cost_values["upper"], cost_values["cost"])
        msg = "Daily AWS cost for `{}` is over the expected range (between {} and {} USD) at {} USD.\n".format(usage_type, cost_values["lower"], cost_values["upper"], cost_values["cost"])

        arcimoto.note.Notification(
                message=msg,
                source=url_string,
                source_type='cost_center'
            )


lambda_handler = utility_notify_aws_cost_and_usage_daily
