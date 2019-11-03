filenum=8
while [ $filenum -le 208 ]
do
	timeout 3 python review-transformer.py $filenum
	filenum=$(($filenum+1))
	echo "Done with $filenum"
done
