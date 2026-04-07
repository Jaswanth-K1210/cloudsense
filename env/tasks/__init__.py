"""Task registry — maps task_id strings to task classes."""

from env.tasks.task_easy import StartupCleanupTask
from env.tasks.task_medium import MidSizeAuditTask
from env.tasks.task_hard import EnterpriseFinOpsTask

TASKS = {
    "startup-cleanup": StartupCleanupTask,
    "mid-size-audit": MidSizeAuditTask,
    "enterprise-finops": EnterpriseFinOpsTask,
}
