Przykładowy output kodu sekwencyjnego:
    Processing CSV files: 100%|██████████| 4/4 [00:50<00:00, 12.72s/it]

    Sequential processing completed in 50.89 seconds.
    Report saved as 'report.txt'.

    Process finished with exit code 0

Przykładowy output z wykorzystaniem ThreadPoolExecutor:
    Processing CSV files: 100%|██████████| 4/4 [00:16<00:00,  4.14s/it]

    Parallel processing completed in 16.59 seconds.
    Report saved as 'report_parallel.txt'.

    Process finished with exit code 0