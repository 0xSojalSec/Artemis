import decouple
from redis import Redis


class Config:
    # Connection string to the MongoDB database
    DB_CONN_STR = decouple.config("DB_CONN_STR", default="")

    # Connection string to Redis store
    REDIS_CONN_STR = decouple.config("REDIS_CONN_STR")

    # An already constructed Redis client
    REDIS = Redis.from_url(decouple.config("REDIS_CONN_STR"))

    # Custom User-Agent string used by Artemis (if not set, the tool defaults will be used: requests, Nuclei etc.)
    CUSTOM_USER_AGENT = decouple.config("CUSTOM_USER_AGENT", default="")

    # Whether we will scan a public suffix (e.g. .pl) if it appears on the target list. This may cause very large
    # number of domains to be scanned.
    ALLOW_SCANNING_PUBLIC_SUFFIXES = decouple.config("ALLOW_SCANNING_PUBLIC_SUFFIXES", default=False, cast=bool)

    # additional domains that will be treated as public suffixes (even though they're not on the default Public Suffix List)
    ADDITIONAL_PUBLIC_SUFFIXES = decouple.config("ADDITIONAL_PUBLIC_SUFFIXES", default="", cast=decouple.Csv(str))

    # What is the maximum task run time (after which it will get killed)
    TASK_TIMEOUT_SECONDS = 4 * 3600

    # By default, Artemis will check whether the reverse DNS lookup for an IP matches
    # the original domain. For example, if we encounter the 1.1.1.1 ip which resolves to
    # new.example.com, Artemis will check whether it is a subdomain of the original task
    # domain.
    #
    # This is to prevent Artemis from randomly walking through the internet after encountering
    # a misconfigured Reverse DNS record (e.g. pointing to a completely different domain).
    #
    # The downside of that is that when you don't provide original domain (e.g. provide
    # an IP to be scanned), the domain from the reverse DNS lookup won't be scanned. Therefore this
    # behavior is configurable and may be turned off.
    VERIFY_REVDNS_IN_SCOPE = decouple.config("VERIFY_REVDNS_IN_SCOPE", default=True, cast=bool)

    # What paths to skip in the robots and directory_index modules
    NOT_INTERESTING_PATHS = decouple.config("NOT_INTERESTING_PATHS", default="/icon/,/icons/", cast=decouple.Csv(str))

    # default request timeout (for all protocols)
    REQUEST_TIMEOUT_SECONDS = decouple.config("REQUEST_TIMEOUT_SECONDS", default=5, cast=int)

    # == Rate limit settings
    # Due to the way this behavior is implemented, we cannot guarantee that a host will never receive more than X
    # requests per second.

    # E.g. when set to 2, Artemis will strive to make no more than one HTTP/MySQL connect/... request per two seconds for any host.
    SECONDS_PER_REQUEST_FOR_ONE_IP = decouple.config("SECONDS_PER_REQUEST_FOR_ONE_IP", default=0, cast=int)

    # E.g. when set to 100, Artemis will strive to send no more than 100 port scanning packets per seconds to any host.
    SCANNING_PACKETS_PER_SECOND_PER_IP = decouple.config("SCANNING_PACKETS_PER_SECOND_PER_IP", default=100, cast=int)

    # Whether Artemis should strive to make at most one module scan a target at a given time
    LOCK_SCANNED_TARGETS = decouple.config("LOCK_SCANNED_TARGETS", default=False, cast=bool)

    # When a resource is locked using artemis.resource_lock.ResourceLock, a retry will be performed in the
    # next LOCK_SLEEP_MIN_SECONDS..LOCK_SLEEP_MAX_SECONDS seconds.
    LOCK_SLEEP_MIN_SECONDS = decouple.config("LOCK_SLEEP_MIN_SECONDS", default=0.1, cast=float)
    LOCK_SLEEP_MAX_SECONDS = decouple.config("LOCK_SLEEP_MAX_SECONDS", default=0.5, cast=float)

    # Amount of times module will try to get a lock on scanned destination (with sleeps inbetween)
    # before rescheduling task for later.
    SCAN_DESTINATION_LOCK_MAX_TRIES = decouple.config("SCAN_DESTINATION_LOCK_MAX_TRIES", default=2, cast=int)

    # Locks are not permanent, because a service that has acquired a lock may get restarted or killed.
    # This is the lock default expiry time.
    DEFAULT_LOCK_EXPIRY_SECONDS = decouple.config("DEFAULT_LOCK_EXPIRY_SECONDS", default=3600, cast=int)

    # In order not to overload the DB and bandwidth, this determines how long
    # the downloaded content would be (in bytes).
    CONTENT_PREFIX_SIZE = decouple.config("CONTENT_PREFIX_SIZE", default=10240, cast=int)

    # == bruter settings (artemis/modules/bruter.py)
    # A threshold in case bruter finds too many files on a server
    # and we want to skip this as a false positive. 0.1 means 10%.
    BRUTER_FALSE_POSITIVE_THRESHOLD = 0.1

    # Each bruter scan would consist of BRUTER_NUM_TOP_PATHS_TO_USE most popular paths that existed on the servers
    # and BRUTER_NUM_RANDOM_PATHS_TO_USE random paths so that we explore random paths from the list to know what
    # would be the most popular paths.
    BRUTER_NUM_TOP_PATHS_TO_USE = decouple.config("BRUTER_NUM_TOP_PATHS_TO_USE", default=800, cast=int)
    BRUTER_NUM_RANDOM_PATHS_TO_USE = decouple.config("BRUTER_NUM_RANDOM_PATHS_TO_USE", default=600, cast=int)

    # If set to True, bruter will follow redirects. If to False, a redirect will be interpreted that a URL
    # doesn't exist, thus decreasing the number of false positives at the cost of losing some true positives.
    BRUTER_FOLLOW_REDIRECTS = decouple.config("BRUTER_FOLLOW_REDIRECTS", default=True, cast=bool)

    # custom port list to scan in CSV form (replaces default list)
    CUSTOM_PORT_SCANNER_PORTS = decouple.config("CUSTOM_PORT_SCANNER_PORTS", default="", cast=decouple.Csv(int))

    # == nuclei settings (artemis/modules/nuclei.py)
    # whether to check that the downloaded Nuclei template list is not empty (may fail e.g. on Github CI when the
    # Github API rate limits are spent)
    NUCLEI_CHECK_TEMPLATE_LIST = decouple.config("NUCLEI_CHECK_TEMPLATE_LIST", default=True, cast=bool)

    # == postman settings (artemis/modules/postman.py)
    # E-mail addresses (from and to) that will be used to test whether a server is an open relay or allows
    # sending e-mails to any address.
    POSTMAN_MAIL_FROM = decouple.config("POSTMAN_MAIL_FROM", default="from@example.com")
    POSTMAN_MAIL_TO = decouple.config("POSTMAN_MAIL_TO", default="to@example.com")

    # == shodan settings (artemis/modules/shodan_vulns.py)
    # Shodan API key so that Shodan vulnerabilities will be displayed in Artemis
    SHODAN_API_KEY = decouple.config("SHODAN_API_KEY", default="")
