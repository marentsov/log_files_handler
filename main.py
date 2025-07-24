from tabulate import tabulate
from src.cli import parse_arguments
from src.log_analyzer import LogAnalyzer


def main():
    args = parse_arguments()
    analyzer = LogAnalyzer()
    analyzer.read_and_safe_logs(args.file)

    data = analyzer.records
    if args.date:
        data = analyzer.filter_by_date(args.date)

    if args.report == "average":
        report = analyzer.generate_average_report(data)
        print(tabulate(
            report,
            headers=["handler", "total", "avg_response_time"],
            showindex=True
        ))


if __name__ == "__main__":
    main()
