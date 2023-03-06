echo 'Start ingestion'
python -m ingestion
echo '--------------------------------'
echo
echo 'Start csv generation'
python -m csv_generator
echo '--------------------------------'