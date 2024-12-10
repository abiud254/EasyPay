from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Allowance(models.Model):
    CALCULATION_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    name = models.CharField(max_length=100, unique=True)
    calculation_type = models.CharField(max_length=15, choices=CALCULATION_TYPES)
    default_value = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} (Default: {self.calculation_type}, {self.default_value})"


class Deduction(models.Model):
    CALCULATION_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    name = models.CharField(max_length=100, unique=True)
    calculation_type = models.CharField(max_length=15, choices=CALCULATION_TYPES)
    default_value = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} (Default: {self.calculation_type}, {self.default_value})"


class JobGroup(models.Model):
    name = models.CharField(max_length=100)
    base_salary = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    allowances = models.ManyToManyField(
        Allowance, through="JobGroupAllowance", related_name="job_groups"
    )
    deductions = models.ManyToManyField(
        Deduction, through="JobGroupDeduction", related_name="job_groups"
    )

    def calculate_total_allowances(self):
        """Calculate the total allowances for this job group."""
        total = Decimal(0)
        for job_group_allowance in self.jobgroupallowance_set.all():
            value = Decimal(job_group_allowance.value)
            if job_group_allowance.calculation_type == "percentage":
                total += (value / Decimal(100)) * Decimal(self.base_salary)
            else:  # Fixed amount
                total += value
        return total

    def calculate_total_deductions(self):
        """Calculate the total deductions for this job group."""
        total = Decimal(0)
        for job_group_deduction in self.jobgroupdeduction_set.all():
            value = Decimal(job_group_deduction.value)
            if job_group_deduction.calculation_type == "percentage":
                total += (value / Decimal(100)) * Decimal(self.base_salary)
            else:  # Fixed amount
                total += value
        return total

    def calculate_net_salary(self):
        """Calculate the net salary after applying allowances and deductions."""
        base_salary = Decimal(self.base_salary)
        total_allowances = self.calculate_total_allowances()
        total_deductions = self.calculate_total_deductions()
        net_salary = base_salary + total_allowances - total_deductions
        return net_salary

    def __str__(self):
        return self.name


class JobGroupAllowance(models.Model):
    CALCULATION_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    job_group = models.ForeignKey(JobGroup, on_delete=models.CASCADE)
    allowance = models.ForeignKey(Allowance, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    calculation_type = models.CharField(
        max_length=15,
        choices=CALCULATION_TYPES,
        default="fixed",  # Default to fixed if not specified
    )

    class Meta:
        unique_together = ("job_group", "allowance")

    def __str__(self):
        return f"{self.allowance.name} ({self.calculation_type}: {self.value}) for {self.job_group.name}"


class JobGroupDeduction(models.Model):
    CALCULATION_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    job_group = models.ForeignKey(JobGroup, on_delete=models.CASCADE)
    deduction = models.ForeignKey(Deduction, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    calculation_type = models.CharField(
        max_length=15,
        choices=CALCULATION_TYPES,
        default="fixed",  # Default to fixed if not specified
    )

    class Meta:
        unique_together = ("job_group", "deduction")

    def __str__(self):
        return f"{self.deduction.name} ({self.calculation_type}: {self.value}) for {self.job_group.name}"


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(models.Model):
    id_number = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    job_group = models.ForeignKey(JobGroup, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id_number})"


class ActivityLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="activity_logs",
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # To log IPs

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"
