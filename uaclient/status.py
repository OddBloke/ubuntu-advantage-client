from datetime import datetime


class TxtColor(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    DISABLEGREY = '\033[37m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


ACTIVE = 'active'
INACTIVE = 'inactive'
INAPPLICABLE = 'inapplicable'
ENTITLED = 'entitled'
UNENTITLED = 'unentitled'
EXPIRED = 'expired'
NONE = 'none'
ESSENTIAL = 'essential'
STANDARD = 'standard'
ADVANCED = 'advanced'

# Colorized status output for terminal
STATUS_COLOR = {
    ACTIVE: TxtColor.OKGREEN + ACTIVE + TxtColor.ENDC,
    INACTIVE: TxtColor.FAIL + INACTIVE + TxtColor.ENDC,
    INAPPLICABLE: TxtColor.DISABLEGREY + INAPPLICABLE + TxtColor.ENDC,
    ENTITLED: TxtColor.OKGREEN + ENTITLED + TxtColor.ENDC,
    UNENTITLED: TxtColor.FAIL + UNENTITLED + TxtColor.ENDC,
    EXPIRED: TxtColor.FAIL + EXPIRED + TxtColor.ENDC,
    NONE: TxtColor.DISABLEGREY + NONE + TxtColor.ENDC,
    ESSENTIAL: TxtColor.OKGREEN + ESSENTIAL + TxtColor.ENDC,
    STANDARD: TxtColor.OKGREEN + STANDARD + TxtColor.ENDC,
    ADVANCED: TxtColor.OKGREEN + ADVANCED + TxtColor.ENDC
}

MESSAGE_DISABLED_TMPL = '{title} disabled.'
MESSAGE_NONROOT_USER = 'This command must be run as root (try using sudo)'
MESSAGE_ALREADY_DISABLED_TMPL = '\
{title} is not currently enabled.\nSee `ua status`'
MESSAGE_ENABLED_FAILED_TMPL = 'Could not enable {title}.'
MESSAGE_ENABLED_TMPL = '{title} enabled.'
MESSAGE_ALREADY_ENABLED_TMPL = '{title} is already enabled.\nSee `ua status`'
MESSAGE_INAPPLICABLE_SERIES_TMPL = '\
{title} is not available for Ubuntu {series}.'
MESSAGE_UNENTITLED_TMPL = """\
This subscription is not entitled to {title}.
See `ua status` or https://ubuntu.com/advantage
"""
MESSAGE_UNATTACHED = """\
This machine is not attached to a UA subscription.

See `ua attach` or https://ubuntu.com/advantage
"""
MESSAGE_MOTD_ACTIVE_TMPL = """
 * This system is covered by Ubuntu Advantage until {date}
Run `ua status` for details.
"""
MESSAGE_MOTD_EXPIRED_TMPL = """
 * Your Ubuntu Advantage subscription {name} expired on {date}!
"""

STATUS_TMPL = '{name: <14}{contract_state: <26}{status}'


def format_entitlement_status(entitlement):
    contract_status = entitlement.contract_status()
    operational_status, _details = entitlement.operational_status()
    fmt_args = {
        'name': entitlement.name,
        'contract_state': STATUS_COLOR.get(contract_status, contract_status),
        'status': STATUS_COLOR.get(operational_status, operational_status)}
    return STATUS_TMPL.format(**fmt_args)


def get_motd_summary(cfg):
    """Return MOTD summary text for all UA entitlements"""
    contracts = cfg.contracts
    if not contracts:
        return ""   # No UA attached, so don't announce anything
    # TODO(Support multiple contracts)
    contractInfo = contracts[0]['contractInfo']
    expiry = datetime.strptime(
        contractInfo['effectiveTo'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if expiry >= datetime.utcnow():
        return MESSAGE_MOTD_ACTIVE_TMPL.format(date=expiry.date())
    else:
        return MESSAGE_MOTD_EXPIRED_TMPL.format(
            name=contractInfo['name'], date=expiry.date())
