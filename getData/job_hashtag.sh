#PBS -l nodes=1:ppn=1 pmem=128mb,pvmem=512mb
#PBS -q shortq
#PBS -l walltime=00:30:00 
#PBS -N twitter_hashtagCount 
#PBS -M xliu15@uvm.edu
#PBS -m a 

cd /users/x/l/xliu15/WORK/hashtagTopic/getData
echo $FILE

gzip -cd ${FILE} | python collect_hashtags.py ${FILE} 

