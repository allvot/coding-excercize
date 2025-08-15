import csv
from typing import Dict, List, Optional
from sort import sort


class Package:
    def __init__(self, width: int, height: int, length: int, mass: int):
        self.width = width
        self.height = height
        self.length = length
        self.mass = mass
        self.volume = width * height * length
        self.sort_value = sort(width, height, length, mass).lower()
        self.is_valid = width > 0 and height > 0 and length > 0 and mass > 0


class CSVProcessorSimple:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.packages: List[Package] = []
        self.statistics: Dict[str, any] = {
            "total_count": 0,
            "standard": {"count": 0, "mass_sum": 0, "volume_sum": 0, "min_mass": None, "max_mass": None, "min_volume": None, "max_volume": None},
            "special": {"count": 0, "mass_sum": 0, "volume_sum": 0, "min_mass": None, "max_mass": None, "min_volume": None, "max_volume": None},
            "rejected": {"count": 0, "mass_sum": 0, "volume_sum": 0, "min_mass": None, "max_mass": None, "min_volume": None, "max_volume": None}
        }

    def create_package(self, row: List[str]) -> Optional[Package]:
        """Create a Package object from CSV row data with proper error handling."""
        try:
            # Skip rows with missing or invalid data
            if len(row) != 4 or any(not cell.strip() for cell in row):
                return None

            # Convert to integers, handling potential conversion errors
            width, height, length, mass = [int(cell.strip()) for cell in row]

            # Create package and validate
            package = Package(width, height, length, mass)
            return package if package.is_valid else None

        except (ValueError, TypeError):
            # Skip rows that can't be converted to integers
            return None

    def update_statistics(self, package: Package) -> None:
        """Update statistics for a valid package."""
        category = package.sort_value

        # Update counts and sums
        self.statistics[category]["count"] += 1
        self.statistics[category]["mass_sum"] += package.mass
        self.statistics[category]["volume_sum"] += package.volume

        # Update min/max values
        if self.statistics[category]["min_mass"] is None:
            self.statistics[category]["min_mass"] = package.mass
            self.statistics[category]["max_mass"] = package.mass
            self.statistics[category]["min_volume"] = package.volume
            self.statistics[category]["max_volume"] = package.volume
        else:
            self.statistics[category]["min_mass"] = min(self.statistics[category]["min_mass"], package.mass)
            self.statistics[category]["max_mass"] = max(self.statistics[category]["max_mass"], package.mass)
            self.statistics[category]["min_volume"] = min(self.statistics[category]["min_volume"], package.volume)
            self.statistics[category]["max_volume"] = max(self.statistics[category]["max_volume"], package.volume)

    def calculate_averages(self) -> None:
        """Calculate average mass and volume for each category, avoiding division by zero."""
        for category in ["standard", "special", "rejected"]:
            count = self.statistics[category]["count"]
            if count > 0:
                self.statistics[category]["average_mass"] = self.statistics[category]["mass_sum"] / count
                self.statistics[category]["average_volume"] = self.statistics[category]["volume_sum"] / count
            else:
                self.statistics[category]["average_mass"] = 0
                self.statistics[category]["average_volume"] = 0

    def process(self) -> Dict[str, any]:
        """Process the CSV file and return statistics."""
        # Use provided file path or default to current directory
        file_path = f"/app/src/{self.file_name}"

        try:
            with open(file_path, "r") as file:
                reader = csv.reader(file)

                # Skip header row
                header = next(reader)
                if len(header) != 4 or not all(col.strip() for col in header):
                    raise ValueError("Invalid CSV header format")

                # Process each row
                for row_num, row in enumerate(reader, start=2):  # Start at 2 to account for header
                    package = self.create_package(row)
                    if package:
                        self.packages.append(package)
                        self.statistics["total_count"] += 1
                        self.update_statistics(package)

                # Calculate final statistics
                self.calculate_averages()

                return self.statistics

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            return {}
        except Exception as e:
            print(f"Error processing file: {e}")
            return {}

    def print_statistics(self) -> None:
        """Print formatted statistics."""
        print(f"Total packages processed: {self.statistics['total_count']}")
        print()

        for category in ["standard", "special", "rejected"]:
            stats = self.statistics[category]
            print(f"{category.title()} packages:")
            print(f"  Count: {stats['count']}")
            if stats['count'] > 0:
                print(f"  Mass: {stats['min_mass']} - {stats['max_mass']} (avg: {stats['average_mass']:.2f})")
                print(f"  Volume: {stats['min_volume']} - {stats['max_volume']} (avg: {stats['average_volume']:.2f})")
            print()


# Example usage
if __name__ == "__main__":
    processor = CSVProcessorSimple("packages.csv")
    stats = processor.process()
    processor.print_statistics()