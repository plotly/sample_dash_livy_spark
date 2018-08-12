class SparkStates:
    NONE = "none"
    STARTING = "starting"
    IDLE = "idle"
    RUNNING = "running"
    DEAD = "dead"


class JobStates:
    NONE = "none"
    OK = "ok"
    AVAILABLE = "available"
    ERROR = "error"


class OutputStatus:
    OK = "ok"


class DashIds:
    SPARK_INFO_INTERVAL = "spark-info-interval"
    JOB_INFO_INTERVAL = "job-info-interval"
    SPARK_SESSION_INFO = "spark-session-state"
    CURRENT_JOB_INFO = "current_job_info"
    CURRENT_STATEMENT_URL = "current_statement_url"
    JOB_OUTPUT = "job_output"
    MODIFIER_SELECT = "modifier-select"
    TRANSFORM_FUNC_SELECT = "transform_func_select"
    RUN_BUTTON = "run-button"
    CHART_1 = "chart-1"
