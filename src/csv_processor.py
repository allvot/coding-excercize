import csv
from sort import sort
from functools import cached_property

class Package:
    def __init__(self, width, height, length, mass):
        self.width = int(width)
        self.height = int(height)
        self.length = int(length)
        self.mass = abs(int(mass))
        self.sort_value = sort(self.width, self.height, self.length, self.mass).lower()
        self.volume = abs(self.width * self.height * self.length)
        self.is_valid = self.width > 0 and self.height > 0 and self.length > 0 and self.mass > 0

class CSVProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.packages = []
        self.statistics = {}
        self.statistics["total_count"] = 0
        self.total_volume = 0
        self.volumes = {}
        self.masses = {}

    def init_package(self, row):
        try:
            package = Package(*[int(column) for column in row])

            if package.is_valid:
                self.packages.append(package)
                return package
        except Exception as error:
            return

    def calculate_sort_count(self, package):
        if self.statistics.get(f"{package.sort_value}_count") is None:
            self.statistics[f"{package.sort_value}_count"] = 0
        if self.volumes.get(f"{package.sort_value}_sum") is None:
            self.volumes[f"{package.sort_value}_sum"] = 0
        if self.masses.get(f"{package.sort_value}_sum") is None:
            self.masses[f"{package.sort_value}_sum"] = 0

    def calculate_min_max(self, unit, package):
        value = getattr(package, unit)

        if self.statistics.get(f"{package.sort_value}_min_{unit}") is None:
            self.statistics[f"{package.sort_value}_min_{unit}"] = value
        else:
            self.statistics[f"{package.sort_value}_min_{unit}"] = min(self.statistics[f"{package.sort_value}_min_{unit}"], value)

        if self.statistics.get(f"{package.sort_value}_max_{unit}") is None:
            self.statistics[f"{package.sort_value}_max_{unit}"] = value
        else:
            self.statistics[f"{package.sort_value}_max_{unit}"] = max(self.statistics[f"{package.sort_value}_max_{unit}"], value)


    def process(self):
        with open(f"/app/src/{self.file_name}", "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                package = self.init_package(row)
                if package is None:
                    continue

                self.statistics["total_count"] += 1

                self.calculate_sort_count(package)
                self.calculate_min_max("mass", package)
                self.calculate_min_max("volume", package)

                self.statistics[f"{package.sort_value}_count"] += 1
                self.volumes[f"{package.sort_value}_sum"] += package.volume
                self.masses[f"{package.sort_value}_sum"] += package.mass

            self.calculate_averages()
            self.print_statistics()
            return self.statistics

    def calculate_averages(self):
        for unit in ["volume", "mass"]:
            for sort_value in ["standard", "special", "rejected"]:
                self.statistics[f"{sort_value}_average_{unit}"] = self.volumes[f"{sort_value}_sum"] / self.statistics[f"{sort_value}_count"]

    def print_statistics(self):
        for key, value in self.statistics.items():
            print(f"{key}: {value}")