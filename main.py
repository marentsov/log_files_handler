from tabulate import tabulate
from src.cli import parse_arguments
from src.log_handler import LogHandler


def main():
    args = parse_arguments()
    handler = LogHandler()
    handler.read_and_safe_logs(args.file)

    data = handler.records
    if args.date:
        data = handler.filter_by_date(args.date)

    if args.report == "average":
        report = handler.generate_average_report(data)
        print(tabulate(
            report,
            headers=["handler", "total", "avg_response_time"],
            showindex=True
        ))


if __name__ == "__main__":
    main()
