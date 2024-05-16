import time

class TimeSystem:
    def __init__(self):
        self.start_time = time.time()
        self.elapsed_time = 0
        self.is_paused = False
        self.seconds_per_minute = 2.5
        self.minutes_per_hour = 60 / self.seconds_per_minute
        self.hours_per_day = 150 / self.seconds_per_minute
        self.days_per_week = 6
        self.weeks_per_month = 5
        self.months_per_year = 12
        self.days_per_year = self.days_per_week * self.weeks_per_month * self.months_per_year
        self.hours_per_year = self.days_per_year * self.hours_per_day

    def update(self):
        if not self.is_paused:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
        return self.elapsed_time

    def get_time(self):
        elapsed_time = self.update()
        total_minutes = elapsed_time / self.seconds_per_minute
        total_hours = total_minutes / 60
        total_days = total_hours / self.hours_per_day
        total_weeks = total_days / self.days_per_week
        total_months = total_weeks / self.weeks_per_month
        total_years = total_months / self.months_per_year

        years = int(total_years)
        months = int(total_months % self.months_per_year)
        weeks = int(total_weeks % self.weeks_per_month)
        days = int(total_days % self.days_per_week)
        hours = int(total_hours % self.hours_per_day)
        minutes = int(total_minutes % 60)

        return {
            "years": years,
            "months": months,
            "weeks": weeks,
            "days": days,
            "hours": hours,
            "minutes": minutes
        }

    def pause(self):
        if not self.is_paused:
            self.is_paused = True
            self.elapsed_time = time.time() - self.start_time

    def resume(self):
        if self.is_paused:
            self.is_paused = False
            self.start_time = time.time() - self.elapsed_time

    def save_time(self):
        return {
            "elapsed_time": self.elapsed_time,
            "is_paused": self.is_paused
        }

    def load_time(self, data):
        self.elapsed_time = data["elapsed_time"]
        self.is_paused = data["is_paused"]
        if not self.is_paused:
            self.start_time = time.time() - self.elapsed_time