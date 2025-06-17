python main.py upload --file sample_data_1.csv
for ((i = 0; i < 15; i++))
do
    python main.py upload --file sample_data_2.csv
done
for ((i = 0; i < 20; i++))
do
    python main.py list
done
for ((i = 1; i < 20; i++))
do
    python main.py export $i
done
for ((i = 15; i < 31; i++))
do
    python main.py stats $i
done
for ((i = 10; i < 26; i++))
do
    python main.py plot $i
done
for ((i = 9; i < 26; i++))
do
    python main.py delete $i
done

sleep 60
for ((i = 0; i < 15; i++))
do
    python main.py upload --file sample_data_1.csv
done
for ((i = 0; i < 20; i++))
do
    python main.py list
done
for ((i = 1; i < 20; i++))
do
    python main.py export $i
done
for ((i = 15; i < 31; i++))
do
    python main.py stats $i
done
for ((i = 10; i < 26; i++))
do
    python main.py plot $i
done
for ((i = 9; i < 26; i++))
do
    python main.py delete $i
done